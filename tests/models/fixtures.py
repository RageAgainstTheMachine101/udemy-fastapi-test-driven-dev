import pytest
from sqlalchemy import inspect


@pytest.fixture(scope="function", autouse=True)
def db_inspector(db_session):
    return inspect(db_session().bind)
