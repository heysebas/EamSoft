# models/base_csv_model.py

import csv
from typing import List, Type, TypeVar, Generic
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)


class BaseCSVModel(Generic[T]):
    def __init__(self, file_path: str, model: Type[T]):
        self.file_path = file_path
        self.model = model

    def leer_todas_las_filas(self) -> List[T]:
        with open(self.file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return [self.model(**row) for row in reader]

    def escribir_fila(self, elemento: T) -> None:
        with open(self.file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=elemento.dict().keys())
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(elemento.dict())
