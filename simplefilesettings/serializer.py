import datetime
import enum
import pathlib
import typing
import inspect

T = typing.TypeVar("T", bound=enum.Enum)


# region: enum


def _serialize_enum(obj: enum.Enum) -> str:
    return obj.value


def _deserialize_enum(value: typing.Union[int, str], obj: typing.Type[T]) -> T:
    return obj(value)


# endregion
# region: datetime


def _serialize_datetime(dt: datetime.datetime) -> str:
    return dt.isoformat()


def _deserialize_datetime(value: str) -> datetime.datetime:
    return datetime.datetime.fromisoformat(value)


def _serialize_timedelta(td: datetime.timedelta) -> float:
    return td.total_seconds()


def _deserialize_timedelta(value: float) -> datetime.timedelta:
    return datetime.timedelta(seconds=value)


def _serialize_date(dt: datetime.date) -> str:
    return dt.isoformat()


def _deserialize_date(value: str) -> datetime.date:
    return datetime.date.fromisoformat(value)


def _serialize_time(dt: datetime.time) -> str:
    return dt.isoformat()


def _deserialize_time(value: str) -> datetime.time:
    return datetime.time.fromisoformat(value)


# endregion
# region: pathlib


def _serialize_pathlib(obj: pathlib.Path) -> str:
    return str(obj)


def _deserialize_pathlib(value: str) -> pathlib.Path:
    return pathlib.Path(value)


# endregion


def serialize(value: typing.Any) -> typing.Any:
    if isinstance(value, enum.Enum):
        return _serialize_enum(value)
    elif isinstance(value, datetime.datetime):
        return _serialize_datetime(value)
    elif isinstance(value, datetime.timedelta):
        return _serialize_timedelta(value)
    elif isinstance(value, datetime.date):
        return _serialize_date(value)
    elif isinstance(value, datetime.time):
        return _serialize_time(value)
    elif isinstance(value, pathlib.Path):
        return _serialize_pathlib(value)
    return value


def deserialize(value: typing.Any, type_hint: typing.Any) -> typing.Any:
    # https://stackoverflow.com/a/395782/9944427
    # Fixes bug where typing.Literal as a type hint would error
    if inspect.isclass(type_hint) and issubclass(type_hint, enum.Enum):
        return _deserialize_enum(value, type_hint)
    elif type_hint == datetime.datetime:
        return _deserialize_datetime(value)
    elif type_hint == datetime.timedelta:
        return _deserialize_timedelta(value)
    elif type_hint == datetime.date:
        return _deserialize_date(value)
    elif type_hint == datetime.time:
        return _deserialize_time(value)
    elif type_hint == pathlib.Path:
        return _deserialize_pathlib(value)
    return value
