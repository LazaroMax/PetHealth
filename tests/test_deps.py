from app import deps


def test_get_db_yields_and_closes_session(monkeypatch):
    """Ejercita get_db() directamente (fuera de las dependencias sobreescritas
    de FastAPI) para cubrir la creación y el cierre de la sesión."""
    from tests.conftest import TestingSessionLocal

    monkeypatch.setattr(deps, "SessionLocal", TestingSessionLocal)

    generator = deps.get_db()
    db = next(generator)
    assert db is not None
    generator.close()
