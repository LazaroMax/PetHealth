def test_create_owner(client, auth_headers):
    response = client.post(
        "/owners/",
        json={"full_name": "Ana López", "email": "ana@example.com", "phone": "555-1234"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["full_name"] == "Ana López"
    assert "id" in data


def test_create_owner_duplicate_email(client, auth_headers):
    client.post(
        "/owners/",
        json={"full_name": "Pedro Gómez", "email": "pedro@example.com"},
        headers=auth_headers,
    )
    response = client.post(
        "/owners/",
        json={"full_name": "Otro Pedro", "email": "pedro@example.com"},
        headers=auth_headers,
    )
    assert response.status_code == 400


def test_list_owners(client, auth_headers):
    client.post(
        "/owners/",
        json={"full_name": "Carlos Ruiz", "email": "carlos@example.com"},
        headers=auth_headers,
    )
    response = client.get("/owners/", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_owner(client, auth_headers):
    create = client.post(
        "/owners/",
        json={"full_name": "Sofía Ramírez", "email": "sofia@example.com"},
        headers=auth_headers,
    )
    owner_id = create.json()["id"]
    response = client.get(f"/owners/{owner_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == owner_id
    assert data["pets"] == []


def test_get_owner_not_found(client, auth_headers):
    response = client.get("/owners/999", headers=auth_headers)
    assert response.status_code == 404


def test_update_owner_not_found(client, auth_headers):
    response = client.put(
        "/owners/999", json={"phone": "555-0000"}, headers=auth_headers
    )
    assert response.status_code == 404


def test_delete_owner_not_found(client, auth_headers):
    response = client.delete("/owners/999", headers=auth_headers)
    assert response.status_code == 404


def test_update_owner(client, auth_headers):
    create = client.post(
        "/owners/",
        json={"full_name": "Luis Pérez", "email": "luis@example.com"},
        headers=auth_headers,
    )
    owner_id = create.json()["id"]
    response = client.put(
        f"/owners/{owner_id}", json={"phone": "555-9999"}, headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["phone"] == "555-9999"


def test_delete_owner(client, auth_headers):
    create = client.post(
        "/owners/",
        json={"full_name": "Marta Gómez", "email": "marta@example.com"},
        headers=auth_headers,
    )
    owner_id = create.json()["id"]
    response = client.delete(f"/owners/{owner_id}", headers=auth_headers)
    assert response.status_code == 204
    response = client.get(f"/owners/{owner_id}", headers=auth_headers)
    assert response.status_code == 404
