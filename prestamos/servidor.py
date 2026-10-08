from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlmodel import Session, select

from prestamos.db import crear_tablas, engine, get_session
from prestamos.modelos import Prestamo


@asynccontextmanager
async def lifespan(app: FastAPI):
    crear_tablas()
    yield


app = FastAPI(title="Préstamos de laboratorio", lifespan=lifespan)


@app.get("/salud")
def salud():
    return {"estado": "ok"}


@app.get("/diagnostico")
def diagnostico():
    return {"motor": engine.dialect.name}


@app.get("/prestamos")
def listar_prestamos(session: Session = Depends(get_session)):
    return session.exec(select(Prestamo)).all()


@app.post("/prestamos")
def crear_prestamo(prestamo: Prestamo, session: Session = Depends(get_session)):
    session.add(prestamo)
    session.commit()
    session.refresh(prestamo)
    return prestamo
