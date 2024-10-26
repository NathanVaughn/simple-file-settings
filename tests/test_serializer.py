import datetime
import enum
import pathlib
import sys
import typing

import pytest

import simplefilesettings.serializer


class EnumTest(enum.Enum):
    A = "A"
    B = "B"


def test_basic_enum() -> None:
    class TestEnum(enum.Enum):
        A = "A"
        B = "B"

    assert simplefilesettings.serializer._serialize_enum(TestEnum.A) == "A"
    assert simplefilesettings.serializer._deserialize_enum("A", TestEnum) == TestEnum.A


@pytest.mark.skipif(sys.version_info < (3, 11), reason="Requires Python 3.11 or higher")
def test_str_enum() -> None:
    class TestEnum(enum.StrEnum):
        A = "A"
        B = "B"

    assert simplefilesettings.serializer._serialize_enum(TestEnum.A) == "A"
    assert simplefilesettings.serializer._deserialize_enum("A", TestEnum) == TestEnum.A


def test_int_enum() -> None:
    class TestEnum(enum.IntEnum):
        A = 1
        B = 2

    assert simplefilesettings.serializer._serialize_enum(TestEnum.A) == 1
    assert simplefilesettings.serializer._deserialize_enum(1, TestEnum) == TestEnum.A


def test_datetime() -> None:
    dt = datetime.datetime.now()
    assert simplefilesettings.serializer._serialize_datetime(dt) == dt.isoformat()
    assert simplefilesettings.serializer._deserialize_datetime(dt.isoformat()) == dt


def test_timedelta() -> None:
    td = datetime.timedelta(days=1, hours=2, minutes=3, seconds=4)
    assert simplefilesettings.serializer._serialize_timedelta(td) == td.total_seconds()
    assert (
        simplefilesettings.serializer._deserialize_timedelta(td.total_seconds()) == td
    )


def test_date() -> None:
    d = datetime.datetime.now().date()
    assert simplefilesettings.serializer._serialize_date(d) == d.isoformat()
    assert simplefilesettings.serializer._deserialize_date(d.isoformat()) == d


def test_time() -> None:
    t = datetime.datetime.now().time()
    assert simplefilesettings.serializer._serialize_time(t) == t.isoformat()
    assert simplefilesettings.serializer._deserialize_time(t.isoformat()) == t


def test_pathlib() -> None:
    p = pathlib.Path(__file__)
    assert simplefilesettings.serializer._serialize_pathlib(p) == str(p)
    assert simplefilesettings.serializer._deserialize_pathlib(str(p)) == p


@pytest.mark.parametrize(
    "given, expected",
    (
        (1, 1),
        (True, True),
        (EnumTest.A, "A"),
        (datetime.datetime(2021, 1, 1, 0, 0, 0), "2021-01-01T00:00:00"),
        (datetime.timedelta(days=1, hours=2, minutes=3, seconds=4), 93784.0),
        (datetime.datetime(2021, 1, 1).date(), "2021-01-01"),
        (datetime.datetime(2021, 1, 1).time(), "00:00:00"),
        (pathlib.Path(__file__), str(pathlib.Path(__file__))),
    ),
)
def test_serializer(given: typing.Any, expected: typing.Any) -> None:
    assert simplefilesettings.serializer.serialize(given) == expected


@pytest.mark.parametrize(
    "given, type_hint, expected",
    (
        (1, int, 1),
        (True, bool, True),
        ("A", EnumTest, EnumTest.A),
        (
            "2021-01-01T00:00:00",
            datetime.datetime,
            datetime.datetime(2021, 1, 1, 0, 0, 0),
        ),
        (
            93784.0,
            datetime.timedelta,
            datetime.timedelta(days=1, hours=2, minutes=3, seconds=4),
        ),
        ("2021-01-01", datetime.date, datetime.datetime(2021, 1, 1).date()),
        ("00:00:00", datetime.time, datetime.datetime(2021, 1, 1).time()),
        (str(pathlib.Path(__file__)), pathlib.Path, pathlib.Path(__file__)),
    ),
)
def test_deserializer(
    given: typing.Any, type_hint: typing.Any, expected: typing.Any
) -> None:
    assert (
        simplefilesettings.serializer.deserialize(given, type_hint=type_hint)
        == expected
    )
