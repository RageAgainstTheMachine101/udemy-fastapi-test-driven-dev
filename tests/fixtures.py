import os

from dotenv import load_dotenv

load_dotenv()

import pytest
from sqlalchemy import create_engine

from .utils.db_utils import migrate_to_db
from .utils.docker_utils import start_db_container

TEST_DB_URL = os.getenv("TEST_DB_URL")


@pytest.fixture(scope="session", autouse=True)
def db_session():
    container = start_db_container()

    engine = create_engine(os.getenv("TEST_DB_URL"))

    with engine.begin() as connection:
        migrate_to_db("migrations", "alembic.ini", connection)

    container.stop()
    container.remove()
