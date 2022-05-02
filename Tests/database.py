#           TESTING DB SETUP            #
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pytest
# working with environment variables
from App.main import app  # import app instance
from App.alchemyModels import Base
from App.database import get_db
from App.config import settings as set

# SAMPLE_URL = 'postgresql://User_name:Password@DB_ipAddress:Port_num/DB_name'
DATABASE_URL = f'postgresql://{set.database_username}:{set.database_password}@{set.database_host}:{set.database_port}/{set.database_name}_test'

engine = create_engine(DATABASE_URL)  # establish connection to db
local_testing_session = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


#               PYTEST FIXTURES         #
@pytest.fixture
def session():
    # Before Tests
    Base.metadata.create_all(bind=engine)  # to initialize database

    db = local_testing_session()
    try:
        yield db    # Tests
    finally:
        db.close()


@pytest.fixture
def client(session):
    # *******   Dependency   ******* #
    def get_test_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = get_test_db

    # Tests
    yield TestClient(app)


@pytest.fixture
def last_client(session):
    # *******   Dependency   ******* #
    def get_test_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = get_test_db

    # Tests
    yield TestClient(app)

    # After Tests
    Base.metadata.drop_all(bind=engine)  # to initialize database
