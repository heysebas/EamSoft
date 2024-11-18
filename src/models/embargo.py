# models/embargo.py

from pydantic import BaseModel, Field
from typing import Optional


class Embargo(BaseModel):
    id_embargo: str = Field(..., alias='id_embargo')
    id_cotizante: str = Field(..., alias='id_cotizante')
    fecha: str
    monto: float

    class Config:
        allow_population_by_field_name = True
        orm_mode = True
