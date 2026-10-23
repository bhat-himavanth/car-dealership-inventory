# ---------- Purchase ----------

def test_purchase_decreases_quantity_by_one(client, user_headers, create_vehicle):
    vehicle = create_vehicle(quantity=3)
    response = client.post(f"/api/vehicles/{vehicle['id']}/purchase", headers=user_headers)

    assert response.status_code == 200
    assert response.json()["quantity"] == 2


def test_cannot_purchase_when_out_of_stock(client, user_headers, create_vehicle):
    vehicle = create_vehicle(quantity=0)
    response = client.post(f"/api/vehicles/{vehicle['id']}/purchase", headers=user_headers)

    assert response.status_code == 400
    assert response.json()["detail"] == "Vehicle is out of stock"


def test_buying_the_last_one_then_again_fails(client, user_headers, create_vehicle):
    vehicle = create_vehicle(quantity=1)
    url = f"/api/vehicles/{vehicle['id']}/purchase"

    assert client.post(url, headers=user_headers).json()["quantity"] == 0
    assert client.post(url, headers=user_headers).status_code == 400


def test_purchase_missing_vehicle_returns_404(client, user_headers):
    assert client.post("/api/vehicles/999/purchase", headers=user_headers).status_code == 404


def test_purchase_requires_login(client):
    assert client.post("/api/vehicles/1/purchase").status_code == 401


# ---------- Restock (admin only) ----------

def test_admin_can_restock(client, admin_headers, create_vehicle):
    vehicle = create_vehicle(quantity=2)
    response = client.post(f"/api/vehicles/{vehicle['id']}/restock", json={"amount": 5}, headers=admin_headers)

    assert response.status_code == 200
    assert response.json()["quantity"] == 7


def test_regular_user_cannot_restock(client, user_headers, create_vehicle):
    vehicle = create_vehicle()
    response = client.post(f"/api/vehicles/{vehicle['id']}/restock", json={"amount": 5}, headers=user_headers)
    assert response.status_code == 403


def test_restock_amount_must_be_positive(client, admin_headers, create_vehicle):
    vehicle = create_vehicle()
    response = client.post(f"/api/vehicles/{vehicle['id']}/restock", json={"amount": 0}, headers=admin_headers)
    assert response.status_code == 422


def test_restock_missing_vehicle_returns_404(client, admin_headers):
    response = client.post("/api/vehicles/999/restock", json={"amount": 5}, headers=admin_headers)
    assert response.status_code == 404