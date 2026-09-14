# PetHealth

[![Tests](https://github.com/LazaroMax/PetHealth/actions/workflows/tests.yml/badge.svg)](https://github.com/LazaroMax/PetHealth/actions/workflows/tests.yml)

API REST para gestión veterinaria construida con **FastAPI**, **SQLAlchemy** y **SQLite**. Proyecto final del curso de Aseguramiento de la Calidad del Software, pensado para practicar pruebas con `pytest` sobre CRUD, autenticación JWT y manejo de contraseñas.

## Recursos

- **Propietarios** (`/owners`): dueños de las mascotas.
- **Mascotas** (`/pets`): pacientes, asociados a un propietario.
- **Citas médicas** (`/appointments`): historial clínico de cada mascota.
- **Autenticación** (`/auth`): registro y login con JWT (contraseñas hasheadas con bcrypt vía passlib).

Todos los endpoints de `owners`, `pets` y `appointments` requieren un token JWT válido en el header `Authorization: Bearer <token>`.

## Instalación

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/macOS

pip install -r requirements.txt
```

## Ejecutar el servidor

```bash
uvicorn app.main:app --reload
```

La API queda disponible en `http://127.0.0.1:8000` y la documentación interactiva (Swagger UI) en `http://127.0.0.1:8000/docs`.

## Uso rápido

1. Registrar usuario: `POST /auth/register` con `{"username": "...", "password": "..."}`
2. Iniciar sesión: `POST /auth/login` (form `x-www-form-urlencoded`) → devuelve `access_token`
3. Usar el token en el header `Authorization: Bearer <token>` para acceder a `/owners`, `/pets` y `/appointments`

## Ejecutar las pruebas

```bash
pytest -v
```

Las pruebas usan una base de datos SQLite en memoria, independiente de `pethealth.db`, por lo que no afectan datos reales ni requieren limpieza manual.
