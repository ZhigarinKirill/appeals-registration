import databases
import sqlalchemy
from sqlalchemy_utils import database_exists, create_database
import uuid
import os

DATABASE_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
DATABASE_USER = os.environ.get('POSTGRES_USER', 'postgres')
DATABASE_PASS = os.environ.get('POSTGRES_PASSWORD', 'postgres')
DATABASE_PORT = os.environ.get('POSTGRES_PORT', 5432)
DATABASE_NAME = os.environ.get('POSTGRES_DB', 'user_appeals')
DATABASE_URL = f'postgresql://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'
# DATABASE_URL = os.environ.get('POSTGRES_URI', 'postgresql://postgres:postgres@localhost:5432/user_appeals')

appeals_database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

appeals_table = sqlalchemy.Table(
    'appeals',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.dialects.postgresql.UUID(), primary_key=True, default=uuid.uuid4),
    sqlalchemy.Column('surname', sqlalchemy.String),
    sqlalchemy.Column('name', sqlalchemy.String),
    sqlalchemy.Column('middle_name', sqlalchemy.String),
    sqlalchemy.Column('text', sqlalchemy.String),
    sqlalchemy.Column('phone', sqlalchemy.String),
    sqlalchemy.Column('email', sqlalchemy.String),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL
)

if not database_exists(engine.url):
    create_database(engine.url)

metadata.create_all(engine)
