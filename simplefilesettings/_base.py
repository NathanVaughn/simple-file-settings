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
        self.__field_defaults = {}

        for name in self.__field_type_hints:
            if name.startswith("_"):
                raise AttributeError(
                    f"Attribute '{name}' cannot start with an underscore"
                )

            try:
                self.__field_defaults[name] = super().__getattribute__(name)
            except AttributeError as e:
                raise AttributeError(
                    f"Missing default value for attribute '{name}'"
                ) from e

        self.__data = {}

    @property
    @abc.abstractmethod
    def _file(self) -> str: ...

    @property
    def _always_read(self) -> bool:
        # sourcery skip: assign-if-exp, reintroduce-else, swap-if-else-branches
        if not hasattr(self.Config, "always_read"):
            return True

        return self.Config.always_read  # type: ignore

    def _read_base(self, loader: Loader, parsing_error: typing.Type[Exception]) -> None:
        # if the file does not exist, return an empty dict
        if not os.path.isfile(self._file):
            self.__data = {}
            return

        try:
            with open(self._file, "rb") as fp:
                fp_data = loader(fp)

            # if we got valid data, but it's not a dict, still trigger error
            if not isinstance(fp_data, dict):
                raise ValueError

            self.__data = fp_data
            return

        except (parsing_error, ValueError):
            # on invalid files, just delete it
            os.remove(self._file)
            self.__data = {}
            return

    @abc.abstractmethod
    def _read(self) -> None: ...

    def _write_base(self, dumper: Dumper) -> None:
        with open(self._file, "w") as fp:
            dumper(self.__data, fp)

    @abc.abstractmethod
    def _write(self) -> None: ...

    def __get(self, key: str, type_hint: typing.Any, default: typing.Any) -> typing.Any:
        # read the file
        if self._always_read or not self.__data:
            self._read()

        # if the requested key is in the config, return it
        if key in self.__data:
            value = self.__data[key]

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
        # make sure value matches the type hint
        typeguard.check_type(value, self.__field_type_hints[key])

        # make sure we have the latest data
        if self._always_read:
            self._read()

        # set value
        self.__data[key] = value
        self._write()

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

    class Config:
        pass
