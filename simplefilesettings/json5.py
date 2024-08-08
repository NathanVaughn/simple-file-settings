import os
import typing

import pyjson5

from simplefilesettings._base import BaseClass, PathLike


class JSON5Class(BaseClass):
    @property
    def _file(self) -> PathLike:
        return self.Config.json5_file

    def _loader_wrapper(self, fp: typing.BinaryIO) -> dict:
        return pyjson5.decode_buffer(fp.read())

    def _read(self) -> None:
        return self._read_base(self._loader_wrapper, pyjson5.Json5DecoderException)

    def _dumper_wrapper(self, obj: dict, fp: typing.TextIO) -> None:
        fp.write(pyjson5.encode(obj))

    def _write(self) -> None:
        return self._write_base(self._dumper_wrapper)

    class Config(BaseClass.Config):
        json5_file: PathLike = os.path.join(os.getcwd(), "settings.json")
