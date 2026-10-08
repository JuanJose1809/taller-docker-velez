## Arranque local

```bash
uv sync
uv run uvicorn prestamos.servidor:app --port 9000
```

`uv sync` crea el entorno `.venv` e instala las versiones exactas que fija `uv.lock`, incluidas las de desarrollo. `requirements.txt` lista solo las dependencias de ejecución, para quien instale con `pip`.

- Salud: `http://127.0.0.1:9000/salud`
- Motor de base de datos en uso: `http://127.0.0.1:9000/diagnostico`
- Registro y listado: `POST` y `GET` en `http://127.0.0.1:9000/prestamos`, con cuerpo `{"equipo": "...", "solicitante": "..."}`

## Pruebas

```bash
uv run pytest
```

## Base de datos

Por defecto persiste en `datos/prestamos.db` (SQLite) y crea la carpeta `datos/` al arrancar. Para usar otro motor, define `PRESTAMOS_DB_URL` antes de arrancar.
