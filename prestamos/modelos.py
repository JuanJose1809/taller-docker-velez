from sqlmodel import Field, SQLModel


class Prestamo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    equipo: str
    solicitante: str
