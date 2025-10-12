"""Base class for engine tests."""

from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def fixture_dir() -> Path:
    """Return the path to the fixture directory."""
    return Path(__file__).parent / "fixtures"
