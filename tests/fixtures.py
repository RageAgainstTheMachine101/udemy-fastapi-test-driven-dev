import pytest

from .utils.docker_utils import start_db_container


@pytest.fixture(scope="session", autouse=True)
def db_session():
    container = start_db_container()
