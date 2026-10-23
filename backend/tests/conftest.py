"""Shared test fixtures.

Each test gets a fresh, empty SQLite database file, so tests never
depend on each other or on your real dealership.db.
"""
import os
import tempfile

# Point the app at a throwaway database BEFORE the app modules are imported.
_test_db_path = os.path.join(tempfile.mkdtemp(), "test.db")
os.environ["DATABASE_URL"] = f"sqlite:///{_test_db_path}"

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.database import Base, SessionLocal, engine  # noqa: E402
from app.main import app  # noqa: E402
from app.models import User  # noqa: E402
from app.security import create_access_token, hash_password  # noqa: E402


@pytest.fixture(autouse=True)
def fresh_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def db():
    session = SessionLocal()
    yield session
    session.close()


def _make_user(db, email, is_admin=False):
    user = User(email=email, hashed_password=hash_password("secret123"), is_admin=is_admin)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def user_headers(db):
    user = _make_user(db, "buyer@example.com")
    return {"Authorization": f"Bearer {create_access_token(user.id)}"}


@pytest.fixture
def admin_headers(db):
    admin = _make_user(db, "admin@example.com", is_admin=True)
    return {"Authorization": f"Bearer {create_access_token(admin.id)}"}


@pytest.fixture
def sample_vehicle():
    return {"make": "Toyota", "model": "Corolla", "category": "Sedan", "price": 20000, "quantity": 3}


@pytest.fixture
def create_vehicle(client, user_headers):
    """Helper that adds a vehicle through the API and returns its JSON."""
    def _create(**overrides):
        data = {"make": "Toyota", "model": "Corolla", "category": "Sedan", "price": 20000, "quantity": 3}
        data.update(overrides)
        response = client.post("/api/vehicles", json=data, headers=user_headers)
        assert response.status_code == 201
        return response.json()
    return _create