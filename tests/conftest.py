import os
import pytest
from sqlalchemy_utils import create_database, drop_database

os.environ['TESTING'] = 'True'

from db.db import TEST_DATABASE_URL


@pytest.fixture(scope="module")
def temp_db():
    create_database(TEST_DATABASE_URL)

    try:
        yield TEST_DATABASE_URL
    finally:
        drop_database(TEST_DATABASE_URL)
