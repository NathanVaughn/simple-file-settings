import pytest

from simplefilesettings.toml import TOMLClass


@pytest.mark.parametrize("temp_file", [("valid.toml")], indirect=["temp_file"])
def test_valid_file(temp_file: str) -> None:
    """
    Ensure normal behavior works.
    """

    class TestClass(TOMLClass):
        key1: str = "default1"
        key2: str = "default2"

        class Config:
            toml_file = temp_file

    tc = TestClass()
    assert tc.key1 == "value1"
    assert tc.key2 == "value2"

    tc.key1 = "newvalue1"
    tc.key2 = "newvalue2"

    assert tc.key1 == "newvalue1"
    assert tc.key2 == "newvalue2"
