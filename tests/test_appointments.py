def _create_owner_and_pet(client, auth_headers):
    owner = client.post(
        "/owners/",
        json={"full_name": "Dueño Cita", "email": "dueno.cita@example.com"},
        headers=auth_headers,
    ).json()
    pet = client.post(
        "/pets/",
        json={"name": "Bobby", "species": "Perro", "owner_id": owner["id"]},
        headers=auth_headers,
    ).json()
    return pet["id"]


def test_create_appointment(client, auth_headers):
    pet_id = _create_owner_and_pet(client, auth_headers)
    response = client.post(
        "/appointments/",
        json={
            "pet_id": pet_id,
            "appointment_date": "2026-01-15T10:00:00",
            "reason": "Vacunación anual",
            "veterinarian": "Dra. Gómez",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    assert response.json()["status"] == "scheduled"


def test_create_appointment_pet_not_found(client, auth_headers):
    response = client.post(
        "/appointments/",
        json={
            "pet_id": 999,
            "appointment_date": "2026-01-15T10:00:00",
            "reason": "Consulta",
        },
        headers=auth_headers,
    )
    assert response.status_code == 404


def test_get_appointment(client, auth_headers):
    pet_id = _create_owner_and_pet(client, auth_headers)
    create = client.post(
        "/appointments/",
        json={
            "pet_id": pet_id,
            "appointment_date": "2026-02-15T09:00:00",
            "reason": "Revisión general",
        },
        headers=auth_headers,
    ).json()
    response = client.get(f"/appointments/{create['id']}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == create["id"]


def test_get_appointment_not_found(client, auth_headers):
    response = client.get("/appointments/999", headers=auth_headers)
    assert response.status_code == 404


def test_update_appointment_not_found(client, auth_headers):
    response = client.put(
        "/appointments/999", json={"status": "completed"}, headers=auth_headers
    )
    assert response.status_code == 404


def test_delete_appointment_not_found(client, auth_headers):
    response = client.delete("/appointments/999", headers=auth_headers)
    assert response.status_code == 404


def test_list_appointments_by_pet(client, auth_headers):
    pet_id = _create_owner_and_pet(client, auth_headers)
    client.post(
        "/appointments/",
        json={
            "pet_id": pet_id,
            "appointment_date": "2026-02-01T09:00:00",
            "reason": "Chequeo",
        },
        headers=auth_headers,
    )
    response = client.get(f"/appointments/?pet_id={pet_id}", headers=auth_headers)
    assert response.status_code == 200
    assert all(a["pet_id"] == pet_id for a in response.json())


def test_update_appointment_diagnosis(client, auth_headers):
    pet_id = _create_owner_and_pet(client, auth_headers)
    create = client.post(
        "/appointments/",
        json={
            "pet_id": pet_id,
            "appointment_date": "2026-03-01T09:00:00",
            "reason": "Consulta",
        },
        headers=auth_headers,
    ).json()
    response = client.put(
        f"/appointments/{create['id']}",
        json={"diagnosis": "Otitis leve", "status": "completed"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["diagnosis"] == "Otitis leve"
    assert response.json()["status"] == "completed"


def test_delete_appointment(client, auth_headers):
    pet_id = _create_owner_and_pet(client, auth_headers)
    create = client.post(
        "/appointments/",
        json={
            "pet_id": pet_id,
            "appointment_date": "2026-04-01T09:00:00",
            "reason": "Consulta",
        },
        headers=auth_headers,
    ).json()
    response = client.delete(f"/appointments/{create['id']}", headers=auth_headers)
    assert response.status_code == 204
