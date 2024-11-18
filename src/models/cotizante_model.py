# models/cotizante_model.py

from models.base_csv_model import BaseCSVModel
from models.cotizante import Cotizante


class CotizanteModel(BaseCSVModel[Cotizante]):
    def __init__(self, file_path: str):
        super().__init__(file_path, Cotizante)
