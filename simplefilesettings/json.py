import json
import os

from simplefilesettings._base import BaseClass, PathLike


class JSONClass(BaseClass):
    @property
    def _file(self) -> PathLike:
        return self.Config.json_file

    def _read(self) -> None:
        return self._read_base(json.load, json.JSONDecodeError)

    def _write(self) -> None:
        return self._write_base(lambda obj, fp: json.dump(obj, fp, indent=4))

    class Config(BaseClass.Config):
        json_file: PathLike = os.path.join(os.getcwd(), "settings.json")
