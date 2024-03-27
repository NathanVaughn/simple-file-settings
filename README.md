# Simple-File-Settings

This is a package intended to easily load and save simple configuration data
transparently through a class.

## Usage

Inherit `simplefilesettings.json.JSONClass` and add class attributes with
type hints and default values. Attributes without type hints will not be
loaded or saved. Attributes without a default value, or starting with an
underscore will cause an error.

```python
from simplefilesettings.json import JSONClass

class _Settings(JSONClass):
    name: str = "John"  # valid
    age = 26 # invalid
    height_cm: int # invalid
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

Nested classes are not supported.

By default, when any attribute is accessed, the configured file will be read. If the file
does not exist, the default value will be used. If the file is not valid JSON,
it will be deleted automatically. To only read the file one time, set the `Config`
value `always_read` to `False`.

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

If JSON isn't your thing, TOML and YAML are available with the `[toml]` and `[yaml]`
extras.

```python
from simplefilesettings.toml import TOMLClass
from simplefilesettings.yaml import YAMLClass

class _TSettings(TOMLClass):
    name: str = "John"

    class Config:
        toml_file = os.path.join(os.path.expanduser("~"), "config.toml")

class _YSettings(YAMLClass):
    name: str = "John"

    class Config:
        yaml_file = os.path.join(os.path.expanduser("~"), "config.yaml")

```

## Development

```bash
python -m pip install pipx --upgrade
pipx ensurepath
pipx install poetry
pipx install vscode-task-runner
# (Optionally) Add pre-commit plugin
poetry self add poetry-pre-commit-plugin
```
