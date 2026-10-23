def register(client, email="new@example.com", password="secret123"):
    return client.post("/api/auth/register", json={"email": email, "password": password})


# ---------- Register ----------

def test_register_creates_user(client):
    response = register(client)

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "new@example.com"
    assert body["is_admin"] is False
    assert "password" not in body and "hashed_password" not in body


def test_register_rejects_duplicate_email(client):
    register(client)
    response = register(client)
    assert response.status_code == 409


def test_register_treats_email_case_insensitively(client):
    register(client, email="Case@Example.com")
    response = register(client, email="case@example.com")
    assert response.status_code == 409


def test_register_rejects_invalid_email(client):
    assert register(client, email="not-an-email").status_code == 422


def test_register_rejects_short_password(client):
    assert register(client, password="123").status_code == 422


# ---------- Login ----------

def test_login_returns_token_and_user(client):
    register(client)
    response = client.post("/api/auth/login", json={"email": "new@example.com", "password": "secret123"})

    assert response.status_code == 200
    body = response.json()
    assert body["access_token"]
    assert body["token_type"] == "bearer"
    assert body["user"]["email"] == "new@example.com"


def test_login_with_wrong_password_fails(client):
    register(client)
    response = client.post("/api/auth/login", json={"email": "new@example.com", "password": "wrong-pass"})
    assert response.status_code == 401


def test_login_with_unknown_email_fails(client):
    response = client.post("/api/auth/login", json={"email": "ghost@example.com", "password": "secret123"})
    assert response.status_code == 401


def test_health_check(client):
    assert client.get("/api/health").json() == {"status": "ok"}