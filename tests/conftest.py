import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


# Capture the initial state of the in-memory activities so tests can reset it.
_initial_activities = copy.deepcopy(app_module.activities)


@pytest.fixture
def client():
    return TestClient(app_module.app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory `activities` dict before each test."""
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(_initial_activities))
    yield
