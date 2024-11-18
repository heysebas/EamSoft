# models/transfer_request.py

from pydantic import BaseModel, Field
from typing import Optional


class TransferRequest(BaseModel):
    id_transfer: str = Field(..., alias='id_transfer')
    id_cotizante: str = Field(..., alias='id_cotizante')
    estado_aprobacion: Optional[str] = Field("Pendiente", alias='estado_aprobacion')

    class Config:
        allow_population_by_field_name = True
        orm_mode = True
