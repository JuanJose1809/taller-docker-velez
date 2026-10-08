from fastapi.testclient import TestClient

from prestamos.servidor import app


def test_salud():
    with TestClient(app) as cliente:
        respuesta = cliente.get("/salud")
    assert respuesta.status_code == 200
    assert respuesta.json() == {"estado": "ok"}


def test_diagnostico_sin_variable_usa_sqlite():
    with TestClient(app) as cliente:
        respuesta = cliente.get("/diagnostico")
    assert respuesta.json() == {"motor": "sqlite"}


def test_crear_y_listar_prestamo():
    with TestClient(app) as cliente:
        creado = cliente.post("/prestamos", json={"equipo": "osciloscopio", "solicitante": "ana"})
        listado = cliente.get("/prestamos")
    assert creado.status_code == 200
    assert creado.json()["id"] is not None
    assert {"equipo": "osciloscopio", "solicitante": "ana"}.items() <= listado.json()[-1].items()
