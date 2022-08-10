from ..__init__ import app
import pytest

app.app_context().push()

@pytest.fixture
def api():
    client = app.test_client()
    return client
