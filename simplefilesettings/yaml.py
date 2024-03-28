import os

import yaml

from simplefilesettings._base import BaseClass, PathLike


class YAMLClass(BaseClass):
    @property
    def _file(self) -> PathLike:
        return self.Config.yaml_file

    def _read(self) -> None:
        return self._read_base(lambda fp: yaml.safe_load(fp), yaml.YAMLError)

    def _write(self) -> None:
        return self._write_base(lambda obj, fp: yaml.dump(obj, fp))

    class Config(BaseClass.Config):
        yaml_file: PathLike = os.path.join(os.getcwd(), "settings.yaml")
