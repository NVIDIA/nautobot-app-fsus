#  SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#  SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
#  NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
#  property and proprietary rights in and to this material, related
#  documentation and any modifications thereto. Any use, reproduction,
#  disclosure or distribution of this material and related documentation
#  without an express license agreement from NVIDIA CORPORATION or
#  its affiliates is strictly prohibited.
"""Task definitions for Invoke."""
import os
from pathlib import Path

from invoke import Collection

from tasks import control
from tasks import test

BASE_DIR = Path(os.path.dirname(__file__)).parent


# Create the namespace here and load the tasks from a module
# to simplify getting them all into the namespace.
namespace: Collection = Collection.from_module(control)
namespace.add_collection(Collection.from_module(test))
namespace.configure(
    {
        "nautobot_fsus": {
            "nautobot_ver": "1.6.28",
            "project_name": "nautobot-fsus",
            "project_source": "nautobot_fsus",
            "python_ver": "3.10",
            "local": False,
            "compose_dir": BASE_DIR.joinpath("development").as_posix(),
            "compose_files": [
                "docker-compose.base.yml",
                "docker-compose.redis.yml",
                "docker-compose.postgres.yml",
                "docker-compose.dev.yml",
            ],
            "compose_http_timeout": "86400",
        },
        "base_dir": BASE_DIR.as_posix(),
    }
)
