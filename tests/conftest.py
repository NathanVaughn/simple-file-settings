import os
import shutil
import tempfile
from typing import Generator

import pytest

TEST_FILES = os.path.join(os.path.dirname(__file__), "files")


@pytest.fixture
def temp_file(request: pytest.FixtureRequest) -> Generator[str, None, None]:
    base_file_path = os.path.join(TEST_FILES, request.param)
    temp_file_path = os.path.join(tempfile.mkdtemp(), request.param)

    # copy the file to a temporary location
    shutil.copy(base_file_path, temp_file_path)
    print(temp_file_path)

    # yield the temporary file
    yield temp_file_path

    # remove the temporary file if it still exists
    shutil.rmtree(os.path.dirname(temp_file_path), ignore_errors=True)
