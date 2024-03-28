import os
import typing

import tomli_w

try:
    import tomllib  # type: ignore
except ImportError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

from simplefilesettings._base import BaseClass, PathLike


class TOMLClass(BaseClass):
    @property
    def _file(self) -> PathLike:
        return self.Config.toml_file

    def _read(self) -> None:
        return self._read_base(lambda fp: tomllib.load(fp), tomllib.TOMLDecodeError)

    def _dumper_wrapper(self, obj: dict, fp: typing.TextIO) -> None:
        fp.write(tomli_w.dumps(obj))

    def _write(self) -> None:
        return self._write_base(self._dumper_wrapper)

    class Config(BaseClass.Config):
        toml_file: PathLike = os.path.join(os.getcwd(), "settings.toml")
