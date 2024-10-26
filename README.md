# Simple-File-Settings

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![GitHub license](https://img.shields.io/github/license/NathanVaughn/simple-file-settings)](https://github.com/NathanVaughn/simple-file-settings/blob/main/LICENSE)
[![PyPi versions](https://img.shields.io/pypi/pyversions/simple-file-settings)](https://pypi.org/project/simple-file-settings)
[![PyPi downloads](https://img.shields.io/pypi/dm/simple-file-settings)](https://pypi.org/project/simple-file-settings)

---

Sometimes, you just need to save and retain a few settings for your desktop program,
like a theme preference, or last viewed directory. This is a library intended
to easily load and save simple configuration data to and from disk through a
type-checked data class.

## Usage

First, a basic use case:

```bash
pip install simple-file-settings
```

```python
import os
from simplefilesettings.json import JSONClass

class _Settings(JSONClass):
    class Config:
        json_file = os.path.join(os.path.expanduser("~"), "config.json")

    mqtt_host: str = "mqtt"
    mqtt_port: int = 1883
    serial_port: str = "COM1"
    serial_baud_rate: int = 115200
    log_file_directory: str = os.path.join(os.getcwd(), "logs")
    force_light_mode: bool = False
    joystick_inverted: bool = False
    max_moving_map_tracks: int = 5000
    takeoff_height: float = 3

Settings = _Settings()

# this will attempt to load the value from the file on disk, or revert to the default
print(Settings.serial_port)

# this will save the change to the config file
Settings.serial_port = "/dev/tty1"
```

Inherit `simplefilesettings.json.JSONClass` and add class attributes with
type hints and optionally default values. Attributes without type hints will
not be loaded or saved. Attributes starting with an underscore will cause an error.
If a default is not provided, `None` is assumed.

```python
from simplefilesettings.json import JSONClass

class _Settings(JSONClass):
    name: str = "John"  # valid
    age = 26 # invalid
    _height_cm: int # invalid
```

By default, a JSON file called `settings.json` in the current working directory
is used. To change this, add a nested class called `Config` with an attribute
`json_file`. This accepts any path-like variable.

```python
import os
from simplefilesettings.json import JSONClass

class _Settings(JSONClass):
    class Config:
        json_file = os.path.join(os.path.expanduser("~"), "config.json")

    name: str = "John"
```

Data types need to serializable for the selected file format
(JSON, TOML, YAML, see below). The following additional types are also supported:

- `datetime.datetime`
- `datetime.date`
- `datetime.time`
- `datetime.timedelta`
- `enum.Enum`
- `pathlib.Path`

By default, when any attribute is accessed, the configured file will be read.
If the file does not exist, the default value will be used.
If the file has a parse error, it will be deleted automatically.
To only read the file one time, set the `Config` value `always_read` to `False`.

When any attribute has its value set, that will be written to the configured file.

```python
from simplefilesettings.json import JSONClass

class _Settings(JSONClass):
    name: str = "John"

Settings = _Settings()
print(Settings.name)
Settings.name = "Bob"
```

Running this twice will print `John` the first time and `Bob` the second time.

If pure JSON isn't your thing, TOML, YAML, and JSON5 are available with the
`[toml]`, `[yaml]`, `[json5]` extras, respectively.

```python
from simplefilesettings.toml import TOMLClass
from simplefilesettings.yaml import YAMLClass
from simplefilesettings.json5 import JSON5Class

class _TSettings(TOMLClass):
    name: str = "Tom"

    class Config:
        toml_file = os.path.join(os.path.expanduser("~"), "config.toml")

class _YSettings(YAMLClass):
    name: str = "Ingy"

    class Config:
        yaml_file = os.path.join(os.path.expanduser("~"), "config.yaml")

class _JSettings(JSON5Class):
    name: str = "Douglas"

    class Config:
        json5_file = os.path.join(os.path.expanduser("~"), "config.jsonc")

```

## Development

Use the provided [devcontainer](https://containers.dev/)
or run the following for local development:

```bash
# Install uv
# https://docs.astral.sh/uv/getting-started/installation/
uv tool install vscode-task-runner
vtr install
```
