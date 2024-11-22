# models/transfer_request.py

# Import required modules
from pydantic import BaseModel, Field  # For data validation and schema definition
from typing import Optional  # For optional fields

# Define the TransferRequest class
# This class represents a transfer request with fields for transfer ID, contributor ID, and approval status.
class TransferRequest(BaseModel):
    # The unique identifier for the transfer
    id_transfer: str = Field(..., alias='id_transfer')
    
    # The identifier for the contributor associated with the transfer
    id_cotizante: str = Field(..., alias='id_cotizante')
    
    # The approval status of the transfer (default: "Pendiente" if not provided)
    estado_aprobacion: Optional[str] = Field("Pendiente", alias='estado_aprobacion')

    # Configuration class for Pydantic
    class Config:
        # Allow access to fields using their names or aliases
        allow_population_by_field_name = True
        
        # Enable compatibility with ORM (Object Relational Mapping) models
        # This is useful if instances of this class need to be created from ORM objects
        orm_mode = True
        