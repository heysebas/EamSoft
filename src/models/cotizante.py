# models/cotizante.py

from pydantic import BaseModel, Field


class Cotizante(BaseModel):
    id_cotizante: str = Field(..., alias='id_cotizante')
    nombre: str
    fondo_actual: str
    desea_transferir: bool

    class Config:
        allow_population_by_field_name = True
        orm_mode = True
