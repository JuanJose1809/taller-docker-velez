import os
from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine

PRESTAMOS_DB_URL = os.environ.get("PRESTAMOS_DB_URL", "sqlite:///./datos/prestamos.db")

connect_args = {"check_same_thread": False} if PRESTAMOS_DB_URL.startswith("sqlite") else {}
engine = create_engine(PRESTAMOS_DB_URL, connect_args=connect_args)


def crear_tablas() -> None:
    if engine.dialect.name == "sqlite":
        Path(engine.url.database).parent.mkdir(exist_ok=True)
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
