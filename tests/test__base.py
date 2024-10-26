import datetime
import enum
import json

import pytest
import typeguard

from simplefilesettings.json import JSONClass


def test_empty_class() -> None:
    """
    Ensure that a class without any attributes raises an error.
    """

    class TestClass(JSONClass):
        pass

    with pytest.raises(TypeError):
        TestClass()


def test_underscore_attribute() -> None:
    """
    Ensure that attributes starting with an underscore raise an error.
    """

    class TestClass(JSONClass):
        _key: int = 1
        key2: str = "default"

    with pytest.raises(AttributeError):
        TestClass()


def test_wrong_set_attribute() -> None:
    """
    Ensure that attributes being set to a value not matching the type
    hint raises and error.
    """

    class TestClass(JSONClass):
        key1: str = "default1"
        key2: str = "default2"

    tc = TestClass()

    with pytest.raises(typeguard.TypeCheckError):
        tc.key1 = True  # type: ignore


@pytest.mark.parametrize("temp_file", [("invalid_syntax.json")], indirect=["temp_file"])
def test_handle_invalid_syntax_file(temp_file: str) -> None:
    """
    Ensure that corrupted files don't cause errors.
    """

    class TestClass(JSONClass):
        key1: str = "default1"
        key2: str = "default2"

        class Config:
            json_file = temp_file

    tc = TestClass()
    assert tc.key1 == "default1"


@pytest.mark.parametrize("temp_file", [("invalid_type.json")], indirect=["temp_file"])
def test_handle_invalid_type_file(temp_file: str) -> None:
    """
    Ensure that files not of the right data type are ignored.
    """

    class TestClass(JSONClass):
        key1: str = "default1"
        key2: str = "default2"

        class Config:
            json_file = temp_file

    tc = TestClass()
    assert tc.key1 == "default1"


@pytest.mark.parametrize("temp_file", [("invalid_empty.json")], indirect=["temp_file"])
def test_handle_invalid_empty_file(temp_file: str) -> None:
    """
    Ensure that empty files are ignored.
    """

    class TestClass(JSONClass):
        key1: str = "default1"
        key2: str = "default2"

        class Config:
            json_file = temp_file

    tc = TestClass()
    assert tc.key1 == "default1"


@pytest.mark.parametrize(
    "temp_file", [("invalid_field_type.json")], indirect=["temp_file"]
)
def test_handle_invalid_field_type_file(temp_file: str) -> None:
    """
    Ensure that files with fields that don't match the type hint are ignored.
    """

    class TestClass(JSONClass):
        key1: str = "default1"
        key2: str = "default2"

        class Config:
            json_file = temp_file

    tc = TestClass()
    assert tc.key1 == "default1"


@pytest.mark.parametrize("temp_file", [("valid.json")], indirect=["temp_file"])
def test_invalid_enum_file(temp_file: str) -> None:
    """
    Ensure that files with invalid enum values are ignored.
    """

    class TestEnum(enum.Enum):
        A = "A"
        B = "B"

    class TestClass(JSONClass):
        key1: TestEnum = TestEnum.B

        class Config:
            json_file = temp_file

    # make sure the default value is used
    tc = TestClass()
    assert tc.key1 == TestEnum.B


@pytest.mark.parametrize("temp_file", [("valid.json")], indirect=["temp_file"])
def test_invalid_datetime_file(temp_file: str) -> None:
    """
    Ensure that files with invalid datetime values are ignored.
    """

    class TestClass(JSONClass):
        key1: datetime.datetime = datetime.datetime(2021, 1, 1, 0, 0, 0)

        class Config:
            json_file = temp_file

    # make sure the default value is used
    tc = TestClass()
    assert tc.key1 == datetime.datetime(2021, 1, 1, 0, 0, 0)


@pytest.mark.parametrize("temp_file", [("valid.json")], indirect=["temp_file"])
def test_valid_file(temp_file: str) -> None:
    """
    Ensure normal behavior works.
    """

    class TestClass(JSONClass):
        key1: str = "default1"
        key2: str = "default2"

        class Config:
            json_file = temp_file

    tc = TestClass()
    assert tc.key1 == "value1"
    assert tc.key2 == "value2"


@pytest.mark.parametrize("temp_file", [("valid.json")], indirect=["temp_file"])
def test_always_read_file(temp_file: str) -> None:
    """
    Ensure always read funtionality works.
    """

    class TestClass(JSONClass):
        key1: str = "default1"
        key2: str = "default2"

        class Config:
            json_file = temp_file
            always_read = True

    tc = TestClass()
    # make sure values are loaded correctly
    assert tc.key1 == "value1"
    assert tc.key2 == "value2"

    # overwrite the file
    with open(temp_file, "w") as fp:
        json.dump({"key1": "newvalue1", "key2": "newvalue2"}, fp)

    # make sure new values are loaded correctly
    assert tc.key1 == "newvalue1"
    assert tc.key2 == "newvalue2"


@pytest.mark.parametrize("temp_file", [("valid.json")], indirect=["temp_file"])
def test_not_always_read_file(temp_file: str) -> None:
    """
    Ensure `always_read` off works.
    """

    class TestClass(JSONClass):
        key1: str = "default1"
        key2: str = "default2"

        class Config:
            json_file = temp_file
            always_read = False

    tc = TestClass()
    # make sure values are loaded correctly
    assert tc.key1 == "value1"
    assert tc.key2 == "value2"

    # overwrite the file
    with open(temp_file, "w") as fp:
        json.dump({"key1": "newvalue1", "key2": "newvalue2"}, fp)

    # make sure new values are NOT loaded
    assert tc.key1 == "value1"
    assert tc.key2 == "value2"


@pytest.mark.parametrize("temp_file", [("valid.json")], indirect=["temp_file"])
def test_writing_value(temp_file: str) -> None:
    """
    Ensure setting attributes updates the file.
    """

    class TestClass(JSONClass):
        key1: str = "default1"
        key2: str = "default2"

        class Config:
            json_file = temp_file
            always_read = False

    tc = TestClass()
    # set values
    tc.key1 = "value1"
    tc.key2 = "value2"

    # make sure the values show up in the file
    with open(temp_file, "r") as fp:
        assert json.load(fp) == {"key1": "value1", "key2": "value2"}


def test_handle_missing_default() -> None:
    """
    Ensure that missing default is None.
    """

    class TestClass(JSONClass):
        key1: int
        key2: str = "default"

    tc = TestClass()
    assert tc.key1 is None


@pytest.mark.parametrize("temp_file", [("valid_2.json")], indirect=["temp_file"])
def test_valid_file_2(temp_file: str) -> None:
    """
    Ensure normal behavior works with enums and other types.
    """

    class TestEnum(enum.Enum):
        A = "A"
        B = "B"

    class TestClass(JSONClass):
        key1: TestEnum = TestEnum.B
        key2: datetime.datetime = datetime.datetime(2021, 1, 1, 0, 0, 0)

        class Config:
            json_file = temp_file

    tc = TestClass()
    assert tc.key1 == TestEnum.A
    assert tc.key2 == datetime.datetime(2024, 2, 3, 5, 3, 0)
