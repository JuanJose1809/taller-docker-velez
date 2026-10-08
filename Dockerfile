# Etapa 1: Obtener la versión oficial de uv
FROM ghcr.io/astral-sh/uv:0.12.17 AS uv

# Etapa 2: Construcción del entorno virtual
FROM python:3.14-slim AS build
COPY --from=uv /uv /usr/local/bin/uv
WORKDIR /app
COPY requirements.txt .
RUN uv venv /opt/venv \
    && uv pip install --python /opt/venv/bin/python --no-cache -r requirements.txt

# Etapa 3: Imagen final de producción
FROM python:3.14-slim
RUN useradd --create-home --uid 1000 appuser

# Copiar únicamente el entorno virtual construido
COPY --from=build /opt/venv /opt/venv

WORKDIR /app

# Copiar paquete prestamos otorgando permisos al usuario appuser
COPY --chown=appuser:appuser prestamos ./prestamos

# Asegurar permisos del directorio de trabajo para SQLite
RUN chown appuser:appuser /app

ENV PATH="/opt/venv/bin:$PATH"
USER appuser

EXPOSE 9000

# Healthcheck que consulta GET /salud
HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:9000/salud')" || exit 1

# Inicio en forma exec apuntando a prestamos.servidor:app
CMD ["uvicorn", "prestamos.servidor:app", "--host", "0.0.0.0", "--port", "9000"]
