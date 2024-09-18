# Installing the App in Nautobot

## Prerequisites

- The App is compatible with Nautobot 1.6.0 and higher.
- Databases supported: PostgreSQL, MySQL.

## Install Guide

!!! note
    Nautobot apps can be installed manually or using Python's `pip`.
    See the [nautobot documentation](https://nautobot.readthedocs.io/en/latest/plugins/#install-the-package) for more details.
    The pip package name for this Nautobot app is [`nautobot-fsus`](https://pypi.org/project/nautobot-fsus/).

The app is available as a Python package via PyPI and can be installed with `pip`:

```shell
pip install nautobot-fsus
```

To ensure the Field Serviceable Units app is automatically re-installed during future upgrades, create a file named `local_requirements.txt` (if not already existing) in the Nautobot root directory (alongside `requirements.txt`) and list the `nautobot-fsus` package:

```shell
echo nautobot-fsus >> local_requirements.txt
```

Once installed, the Nautobot app needs to be enabled in your Nautobot configuration.
The following block of code below shows the additional configuration required to be added to your `nautobot_config.py` file:

- Append `"nautobot_fsus"` to the `PLUGINS` list.

```python
# In your nautobot_config.py
PLUGINS = ["nautobot_fsus"]
```

Once the Nautobot configuration is updated, run the Post Upgrade command (`nautobot-server post_upgrade`) to run migrations and clear any cache:

```shell
nautobot-server post_upgrade
```

Then restart (if necessary) the Nautobot services which may include:

- Nautobot
- Nautobot Workers
- Nautobot Scheduler

```shell
sudo systemctl restart nautobot nautobot-worker nautobot-scheduler
```
