# models/super_cache.py

from typing import Dict, List, Any
from models.base_csv_model import BaseCSVModel
from pydantic import BaseModel


class SuperCache:
    def __init__(self):
        self.cache: Dict[str, List[Dict[str, Any]]] = {}

    def cargar_csv(self, file_name: str, model: BaseCSVModel):
        self.cache[file_name] = [item.dict() for item in model.leer_todas_las_filas()]

    def obtener_cache(self, file_name: str) -> List[Dict[str, Any]]:
        return self.cache.get(file_name, [])
