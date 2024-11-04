import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from testcontainers.postgres import PostgresContainer
from sqlalchemy.orm import Session
from uuid import uuid4

from app.core.db import Base
from app.deps import get_db
from app.main import user_app as app
from app import models

postgres = PostgresContainer()


@pytest.fixture(name="db", scope="session", autouse=True)
def db(request: pytest.FixtureRequest):
    """
    Fixture to create a database session for the test session.

    This fixture starts a PostgreSQL container, creates a database session, and yields it for use in tests.
    After the test session, it stops the PostgreSQL container.
    """
    postgres.start()
    def remove_container():
        postgres.stop()
    request.addfinalizer(remove_container)
    db_url = postgres.get_connection_url()
    engine = create_engine(db_url)
    Base.metadata.create_all(engine, checkfirst=True) 
    with Session(engine) as session:
        yield session


@pytest.fixture
def client(db: Session):
    """
    Fixture to create a test client for the FastAPI application.

    This fixture creates a test client with a test database session, overrides the database
    dependency, and cleans up after the test. It depends on the db fixture to provide
    the test database session.
    """
    # Override the get_db dependency to use the test database
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
            
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clear any overrides after the test
    app.dependency_overrides.clear()


@pytest.fixture
def user(db: Session):
    """Fixture to create a test user"""
    user = models.User(
        email="user@example.com",
        fullname="Test User",
        nickname="tester"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def api_key(db: Session, user: models.User):
    """Fixture to create a test API key for the test user"""
    key = models.ApiKey(
        user_id=user.id,
        key=str(uuid4()),
        name="Test Key"
    )
    db.add(key)
    db.commit()
    db.refresh(key)
    return key
