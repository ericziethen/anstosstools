
from pathlib import Path
import pytest


def pytest_collection_modifyitems(items):
    for item in items:
        # Mark tests in integration folder to not count towards coverage
        if "integration" in Path(item.fspath).parts:
            item.add_marker(pytest.mark.no_cover)
