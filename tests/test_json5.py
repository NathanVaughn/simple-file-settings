import pytest

from simplefilesettings.json5 import JSON5Class


@pytest.mark.parametrize("temp_file", [("valid.jsonc")], indirect=["temp_file"])
def test_valid_file(temp_file: str) -> None:
    """
    Ensure normal behavior works.
    """

    class TestClass(JSON5Class):
        key1: str = "default1"
        key2: str = "default2"

        class Config:
            json5_file = temp_file

    tc = TestClass()
    assert tc.key1 == "value1"
    assert tc.key2 == "value2"

    tc.key1 = "newvalue1"
    tc.key2 = "newvalue2"

    assert tc.key1 == "newvalue1"
    assert tc.key2 == "newvalue2"
