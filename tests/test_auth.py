from app.security import create_access_token


def test_register_new_user(client):
    response = client.post(
        "/auth/register", json={"username": "nuevo_usuario", "password": "clave123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "nuevo_usuario"
    assert "password" not in data
    assert "hashed_password" not in data


def test_register_duplicate_username(client):
    client.post(
        "/auth/register", json={"username": "duplicado", "password": "clave123"}
    )
    response = client.post(
        "/auth/register", json={"username": "duplicado", "password": "otraClave"}
    )
    assert response.status_code == 400


def test_login_success(client):
    client.post(
        "/auth/register", json={"username": "loginuser", "password": "clave123"}
    )
    response = client.post(
        "/auth/login", data={"username": "loginuser", "password": "clave123"}
    )
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post(
        "/auth/register", json={"username": "loginuser2", "password": "clave123"}
    )
    response = client.post(
        "/auth/login", data={"username": "loginuser2", "password": "incorrecta"}
    )
    assert response.status_code == 401


def test_login_nonexistent_user(client):
    response = client.post(
        "/auth/login", data={"username": "no_existe", "password": "clave123"}
    )
    assert response.status_code == 401


def test_protected_endpoint_without_token(client):
    response = client.get("/owners/")
    assert response.status_code == 401


def test_protected_endpoint_with_invalid_token(client):
    response = client.get(
        "/owners/", headers={"Authorization": "Bearer token-invalido"}
    )
    assert response.status_code == 401


def test_token_without_sub_claim(client):
    """Un token válido (bien firmado) pero sin el claim 'sub' debe rechazarse."""
    token = create_access_token(data={"foo": "bar"})
    response = client.get("/owners/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401


def test_token_for_nonexistent_user(client):
    """Un token válido cuyo usuario ya no existe en la base de datos debe rechazarse."""
    token = create_access_token(data={"sub": "usuario_fantasma"})
    response = client.get("/owners/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
