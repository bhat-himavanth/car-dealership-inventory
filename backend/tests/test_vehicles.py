import pytest


# ---------- Protection ----------

@pytest.mark.parametrize("method, url", [
    ("get", "/api/vehicles"),
    ("post", "/api/vehicles"),
    ("get", "/api/vehicles/search"),
    ("put", "/api/vehicles/1"),
    ("delete", "/api/vehicles/1"),
])
def test_vehicle_routes_require_login(client, method, url):
    response = getattr(client, method)(url)
    assert response.status_code == 401


def test_garbage_token_is_rejected(client):
    response = client.get("/api/vehicles", headers={"Authorization": "Bearer not.a.token"})
    assert response.status_code == 401


def test_token_from_login_unlocks_protected_routes(client):
    client.post("/api/auth/register", json={"email": "new@example.com", "password": "secret123"})
    token = client.post(
        "/api/auth/login", json={"email": "new@example.com", "password": "secret123"}
    ).json()["access_token"]

    response = client.get("/api/vehicles", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


# ---------- Create ----------

def test_add_vehicle(client, user_headers, sample_vehicle):
    response = client.post("/api/vehicles", json=sample_vehicle, headers=user_headers)

    assert response.status_code == 201
    body = response.json()
    assert body["id"] > 0
    assert body["make"] == "Toyota"
    assert body["quantity"] == 3


@pytest.mark.parametrize("bad_field", [
    {"price": 0},
    {"price": -500},
    {"quantity": -1},
    {"make": ""},
])
def test_add_vehicle_rejects_invalid_data(client, user_headers, sample_vehicle, bad_field):
    response = client.post("/api/vehicles", json={**sample_vehicle, **bad_field}, headers=user_headers)
    assert response.status_code == 422


def test_add_vehicle_requires_all_fields(client, user_headers):
    response = client.post("/api/vehicles", json={"make": "Toyota"}, headers=user_headers)
    assert response.status_code == 422


# ---------- List ----------

def test_list_is_empty_at_start(client, user_headers):
    assert client.get("/api/vehicles", headers=user_headers).json() == []


def test_list_returns_added_vehicles(client, user_headers, create_vehicle):
    create_vehicle(make="Toyota")
    create_vehicle(make="Honda")

    makes = [v["make"] for v in client.get("/api/vehicles", headers=user_headers).json()]
    assert makes == ["Toyota", "Honda"]


# ---------- Search ----------

@pytest.fixture
def showroom(create_vehicle):
    create_vehicle(make="Toyota", model="Corolla", category="Sedan", price=20000)
    create_vehicle(make="Toyota", model="Fortuner", category="SUV", price=45000)
    create_vehicle(make="Honda", model="City", category="Sedan", price=15000)


def search(client, headers, **params):
    response = client.get("/api/vehicles/search", params=params, headers=headers)
    assert response.status_code == 200
    return [v["model"] for v in response.json()]


def test_search_by_make_is_case_insensitive(client, user_headers, showroom):
    assert search(client, user_headers, make="toyota") == ["Corolla", "Fortuner"]


def test_search_by_partial_model(client, user_headers, showroom):
    assert search(client, user_headers, model="fort") == ["Fortuner"]


def test_search_by_category(client, user_headers, showroom):
    assert search(client, user_headers, category="sedan") == ["Corolla", "City"]


def test_search_by_price_range(client, user_headers, showroom):
    assert search(client, user_headers, min_price=16000, max_price=50000) == ["Corolla", "Fortuner"]


def test_search_combines_filters(client, user_headers, showroom):
    assert search(client, user_headers, make="toyota", category="suv") == ["Fortuner"]


def test_search_without_filters_returns_everything(client, user_headers, showroom):
    assert len(search(client, user_headers)) == 3


def test_search_with_no_match_returns_empty_list(client, user_headers, showroom):
    assert search(client, user_headers, make="Ferrari") == []


# ---------- Update ----------

def test_update_changes_only_given_fields(client, user_headers, create_vehicle):
    vehicle = create_vehicle()
    response = client.put(f"/api/vehicles/{vehicle['id']}", json={"price": 18500}, headers=user_headers)

    assert response.status_code == 200
    body = response.json()
    assert body["price"] == 18500
    assert body["make"] == "Toyota"  # untouched


def test_update_rejects_invalid_price(client, user_headers, create_vehicle):
    vehicle = create_vehicle()
    response = client.put(f"/api/vehicles/{vehicle['id']}", json={"price": -1}, headers=user_headers)
    assert response.status_code == 422


def test_update_missing_vehicle_returns_404(client, user_headers):
    response = client.put("/api/vehicles/999", json={"price": 100}, headers=user_headers)
    assert response.status_code == 404


# ---------- Delete (admin only) ----------

def test_regular_user_cannot_delete(client, user_headers, create_vehicle):
    vehicle = create_vehicle()
    response = client.delete(f"/api/vehicles/{vehicle['id']}", headers=user_headers)
    assert response.status_code == 403


def test_admin_can_delete(client, user_headers, admin_headers, create_vehicle):
    vehicle = create_vehicle()
    response = client.delete(f"/api/vehicles/{vehicle['id']}", headers=admin_headers)

    assert response.status_code == 204
    assert client.get("/api/vehicles", headers=user_headers).json() == []


def test_delete_missing_vehicle_returns_404(client, admin_headers):
    assert client.delete("/api/vehicles/999", headers=admin_headers).status_code == 404