def _create_owner(client, auth_headers):
    response = client.post(
        "/owners/",
        json={"full_name": "Dueño de Prueba", "email": "dueno@example.com"},
        headers=auth_headers,
    )
    return response.json()["id"]


def test_create_pet(client, auth_headers):
    owner_id = _create_owner(client, auth_headers)
    response = client.post(
        "/pets/",
        json={
            "name": "Firulais",
            "species": "Perro",
            "breed": "Labrador",
            "age": 3,
            "owner_id": owner_id,
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Firulais"


def test_create_pet_owner_not_found(client, auth_headers):
    response = client.post(
        "/pets/",
        json={"name": "Michi", "species": "Gato", "owner_id": 999},
        headers=auth_headers,
    )
    assert response.status_code == 404


def test_list_pets_by_owner(client, auth_headers):
    owner_id = _create_owner(client, auth_headers)
    client.post(
        "/pets/",
        json={"name": "Rocky", "species": "Perro", "owner_id": owner_id},
        headers=auth_headers,
    )
    response = client.get(f"/pets/?owner_id={owner_id}", headers=auth_headers)
    assert response.status_code == 200
    assert all(pet["owner_id"] == owner_id for pet in response.json())


def test_get_pet_with_appointments(client, auth_headers):
    owner_id = _create_owner(client, auth_headers)
    pet = client.post(
        "/pets/",
        json={"name": "Coco", "species": "Perro", "owner_id": owner_id},
        headers=auth_headers,
    ).json()
    response = client.get(f"/pets/{pet['id']}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["appointments"] == []


def test_get_pet_not_found(client, auth_headers):
    response = client.get("/pets/999", headers=auth_headers)
    assert response.status_code == 404


def test_update_pet_not_found(client, auth_headers):
    response = client.put("/pets/999", json={"age": 2}, headers=auth_headers)
    assert response.status_code == 404


def test_delete_pet_not_found(client, auth_headers):
    response = client.delete("/pets/999", headers=auth_headers)
    assert response.status_code == 404


def test_update_pet(client, auth_headers):
    owner_id = _create_owner(client, auth_headers)
    create = client.post(
        "/pets/",
        json={"name": "Toby", "species": "Perro", "owner_id": owner_id},
        headers=auth_headers,
    )
    pet_id = create.json()["id"]
    response = client.put(f"/pets/{pet_id}", json={"age": 5}, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["age"] == 5


def test_delete_pet(client, auth_headers):
    owner_id = _create_owner(client, auth_headers)
    create = client.post(
        "/pets/",
        json={"name": "Nina", "species": "Gata", "owner_id": owner_id},
        headers=auth_headers,
    )
    pet_id = create.json()["id"]
    response = client.delete(f"/pets/{pet_id}", headers=auth_headers)
    assert response.status_code == 204
