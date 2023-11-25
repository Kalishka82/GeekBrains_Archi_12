from os import environ
from settings import settings

import databases
import sqlalchemy

DATABASE_URL = settings.DATABASE_URL
TEST_DATABASE_URL = settings.TEST_DATABASE_URL
metadata = sqlalchemy.MetaData()

clients = sqlalchemy.Table(
    "clients",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("document", sqlalchemy.String(300), nullable=False),
    sqlalchemy.Column("lastname", sqlalchemy.String(80), nullable=False),
    sqlalchemy.Column("firstname", sqlalchemy.String(80), nullable=False),
    sqlalchemy.Column("midname", sqlalchemy.String(80), nullable=False),
    sqlalchemy.Column("birthday", sqlalchemy.Date, nullable=False),
)

pets = sqlalchemy.Table(
    "pets",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("client_id", sqlalchemy.ForeignKey("clients.id"), nullable=False),
    sqlalchemy.Column("name", sqlalchemy.String(80), nullable=False),
    sqlalchemy.Column("birthday", sqlalchemy.Date, nullable=False),
)

consultations = sqlalchemy.Table(
    "consultations",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("client_id", sqlalchemy.ForeignKey("clients.id"), nullable=False),
    sqlalchemy.Column("pet_id", sqlalchemy.ForeignKey("pets.id"), nullable=False),
    sqlalchemy.Column("date_time", sqlalchemy.DateTime, nullable=False),
    sqlalchemy.Column("description", sqlalchemy.String(300), nullable=True),
)

TESTING = environ.get("TESTING")

if TESTING:
    database = databases.Database(TEST_DATABASE_URL)
    engine = sqlalchemy.create_engine(
        TEST_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    database = databases.Database(DATABASE_URL)
    engine = sqlalchemy.create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )

metadata.create_all(engine)
