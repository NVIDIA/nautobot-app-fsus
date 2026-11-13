#  SPDX-FileCopyrightText: Copyright (c) "2024" NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#  SPDX-License-Identifier: Apache-2.0
#
#  Licensed under the Apache License, Version 2.0 (the "License")
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""Test runner wrapper for Nautobot FSUs app."""

import copy
import re

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from django.db import connections
from django.test import runner as django_test_runner
from django.test.utils import override_settings
from django_redis import get_redis_connection
from redis import RedisError
from xmlrunner.extra.djangotestrunner import XMLTestRunner

# Redis ships with 16 logical databases by default. Each parallel test worker
# claims `base cache db + worker id` (see _init_prismo_worker), so the worker
# count must stay within the addressable range above the base database.
REDIS_DEFAULT_DATABASE_COUNT = 16


def _redis_database_count():
    """Return the number of logical databases on the cache Redis server.

    Queried live so a server configured with more databases allows more
    workers. CONFIG can be disabled on hardened or managed Redis deployments,
    and the cache backend may not be Redis at all, so any discovery failure
    falls back to the Redis default rather than breaking the test run.
    """
    try:
        return int(get_redis_connection("default").config_get("databases")["databases"])
    except (ImproperlyConfigured, NotImplementedError, KeyError, ValueError, RedisError):
        return REDIS_DEFAULT_DATABASE_COUNT


def _base_cache_db(location):
    """Return the Redis database index in a cache LOCATION (0 when absent)."""
    match = re.search(r"/(\d+)$", location)
    return int(match.group(1)) if match else 0


def _worker_cache_location(location, worker_id):
    """Return the cache LOCATION rewritten to a Redis database unique to the worker.

    A trailing `/<db>` is offset by the worker id; a LOCATION without a database
    index is treated as database 0.
    """
    worker_db = _base_cache_db(location) + worker_id
    if re.search(r"/\d+$", location):
        return re.sub(r"/\d+$", f"/{worker_db}", location)
    return f"{location}/{worker_db}"


def _init_fsu_worker(counter, *args, **kwargs):
    """Initialize a parallel test worker with an isolated Redis cache database.

    Nautobot's test setUp calls cache.clear(), which django-redis implements as
    FLUSHDB. With workers sharing one Redis database, each worker's clear wipes
    every other worker's cache mid-test (breaking, e.g., query-count assertions),
    so each worker is moved onto its own Redis database after Django's standard
    worker setup assigns the worker id.
    """
    # pylint: disable-next=protected-access
    django_test_runner._init_worker(counter, *args, **kwargs)

    caches_config = copy.deepcopy(settings.CACHES)
    for config in caches_config.values():
        config["LOCATION"] = _worker_cache_location(
            config.get("LOCATION", ""),
            django_test_runner._worker_id,  # pylint: disable=protected-access
        )

    # enable() re-points settings.CACHES and signals Django to rebuild cache
    # connections; never disabled because the worker process is single-use.
    override_settings(CACHES=caches_config).enable()


def max_parallel_workers():
    """Return the highest worker count the configured cache databases allow.

    Workers claim `base cache db + worker id`, so a higher configured base
    database leaves fewer databases for workers.
    """
    highest_base = max(
        (_base_cache_db(config.get("LOCATION", "")) for config in settings.CACHES.values()),
        default=0,
    )
    return max(_redis_database_count() - 1 - highest_base, 0)


class FSUParallelTestSuite(django_test_runner.ParallelTestSuite):
    """ParallelTestSuite whose workers get isolated Redis cache databases."""

    init_worker = _init_fsu_worker


class NautobotFSUsTestRunner(XMLTestRunner):
    """
    Version of the NautobotTestRunner that doesn't flush the database by default.
    """

    parallel_test_suite = FSUParallelTestSuite

    def __init__(self, cache_test_fixtures=False, **kwargs):
        self.cache_test_fixtures = cache_test_fixtures
        self.fixture_file = kwargs.get("fixture_file", "development/factory_dump.json")
        self.report_file = kwargs.get("report_file")
        self.flush = kwargs.get("flush")
        self.keepdb = kwargs.get("keepdb")

        # Assert "integration" hasn't been provided w/ --tag
        incoming_tags = kwargs.get("tags") or []
        # Assert "exclude_tags" hasn't been provided w/ --exclude-tag; else default to our own.
        incoming_exclude_tags = kwargs.get("exclude_tags") or []

        # Only include our excluded tags if "integration" isn't provided w/ --tag
        if "integration" not in incoming_tags:
            incoming_exclude_tags.append("integration")
            kwargs["exclude_tags"] = incoming_exclude_tags

        super().__init__(**kwargs)

        # Each worker needs its own Redis database above the configured base
        # database; see max_parallel_workers().
        self.parallel = min(self.parallel, max_parallel_workers())

    @classmethod
    def add_arguments(cls, parser):
        """Additional arguments for the test runner."""
        super().add_arguments(parser)
        parser.add_argument(
            "--cache-test-fixtures",
            action="store_true",
            help="Save test database to a json fixture file to re-use on subsequent tests.",
        )
        parser.add_argument(
            "--fixture-file",
            default="development/factory_dump.json",
            help="Fixture file to use with --cache-test-fixtures.",
        )
        parser.add_argument(
            "--report-file", default="rspec.xml", help="Filename for the saved XML test report."
        )
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Flush any existing data in the database before generating new test data.",
        )

    def setup_test_environment(self, **kwargs):
        """Global pre-test setup."""
        super().setup_test_environment(**kwargs)

        # Remove 'testserver' that Django "helpfully" adds automatically
        # to ALLOWED_HOSTS, masking issues like #3065
        settings.ALLOWED_HOSTS.remove("testserver")

        # Update the XMLTestRunner settings if needed.
        settings.TEST_OUTPUT_VERBOSE = self.verbosity
        if self.report_file is not None:
            settings.TEST_OUTPUT_FILE_NAME = self.report_file

    def setup_databases(self, **kwargs):
        """Create the test databases and add base set of factory data."""
        # Suppress parallel cloning during creation: Django clones the test database
        # inside super().setup_databases(), which would snapshot it before
        # create_fsus_env seeds it. Seed first, then clone for the workers below.
        requested_parallel = self.parallel
        self.parallel = 0
        try:
            result = super().setup_databases(**kwargs)
        finally:
            self.parallel = requested_parallel

        if result:
            command = ["create_fsus_env", "--flush", "--no-input"]
            if settings.TEST_FACTORY_SEED is not None:
                command.extend(["--seed", settings.TEST_FACTORY_SEED])
            if self.cache_test_fixtures:
                command.append("--cache-fixtures")
            if self.fixture_file:
                command.extend(["--fixture-file", self.fixture_file])

            for connection in result:
                alias = connection[0].alias
                print(f"  Pre-populating test database {alias}...")
                db_command = [*command, "--database", alias]
                call_command(*db_command)

        if self.parallel > 1 and result:
            for connection in result:
                for index in range(1, requested_parallel + 1):
                    # keepdb is intentionally not honored for the clones: a kept clone
                    # would retain data from a previous run instead of copying the
                    # freshly re-seeded primary. Re-cloning costs well under a second.
                    connection[0].creation.clone_test_db(
                        suffix=str(index), verbosity=self.verbosity, keepdb=False
                    )

        return result

    def teardown_databases(self, old_config, **kwargs):
        """Clean up the test databases."""
        # Under --parallel, forked workers inherit the parent's DB sockets and their
        # worker setup closes them, terminating the parent's sessions server-side.
        # Drop the dead connections so the flush below opens fresh ones.
        if self.parallel > 1:
            connections.close_all()

        # If keepdb is set, the test database won't be dropped, so we'll clean up the test data.
        if self.keepdb:
            command = ["flush_fsus_env", "--no-input"]
            for connection in old_config:
                db_name = connection[0].alias
                print(f"Cleaning up test database {db_name}...")
                db_command = command + ["--database", db_name]
                call_command(*db_command)

        super().teardown_databases(old_config, **kwargs)
