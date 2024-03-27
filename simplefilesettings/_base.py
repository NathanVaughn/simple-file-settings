import abc
import contextlib
import os
import typing

import typeguard

PathLike = typing.Union[str, os.PathLike]
ParseFloat = typing.Callable[[str], typing.Any]


class Loader(typing.Protocol):
    def __call__(self, fp: typing.BinaryIO) -> dict: ...


class Dumper(typing.Protocol):
    def __call__(self, obj: dict, fp: typing.TextIO) -> None: ...


class BaseClass(abc.ABC):
    def __init__(self):
        self.__field_type_hints = typing.get_type_hints(self)
        self.__field_defaults = {
            name: super().__getattribute__(name) for name in self.__field_type_hints
        }

    @property
    @abc.abstractmethod
    def _file(self) -> str: ...

    def _read_base(self, loader: Loader, parsing_error: typing.Type[Exception]) -> dict:
        # if the file does not exist, return an empty dict
        if not os.path.isfile(self._file):
            return {}

        try:
            with open(self._file, "rb") as fp:
                data = loader(fp)

            # if we got valid data, but it's not a dict, still trigger error
            if not isinstance(data, dict):
                raise ValueError

            return data

        except (parsing_error, ValueError):
            # on invalid files, just delete it
            os.remove(self._file)
            return {}

    @abc.abstractmethod
    def _read(self) -> dict: ...

    def _write_base(self, data: dict, dumper: Dumper) -> None:
        with open(self._file, "w") as fp:
            dumper(data, fp)

    @abc.abstractmethod
    def _write(self, data: dict) -> None: ...

    def __get(self, key: str, type_hint: typing.Any, default: typing.Any) -> typing.Any:
        # read the file
        data = self._read()

        # if the requested key is in the config, return it
        if key in data:
            value = data[key]

            with contextlib.suppress(typeguard.TypeCheckError):
                # make sure the value is of the correct type
                # otherwise, return the default
                typeguard.check_type(value, type_hint)
                return value

        # if we have a set default value that is not None, write it out
        if default is not None:
            self.__set(key, default)

        return default

    def __set(self, key: str, value: typing.Any) -> None:
        data = self._read()
        data[key] = value
        self._write(data)

    def __getattribute__(self, name: str) -> typing.Any:
        # private attribute or outside our scope access normally
        if name.startswith("_") or name not in self.__field_type_hints:
            return super().__getattribute__(name)

        # declared field
        return self.__get(
            name, self.__field_type_hints[name], self.__field_defaults[name]
        )

    def __setattr__(self, name: str, value: typing.Any) -> None:
        # private attribute or outside our scope access normally
        if name.startswith("_") or name not in self.__field_type_hints:
            return super().__setattr__(name, value)

        # declared field
        self.__set(name, value)
