# models/embargo_model.py

from models.base_csv_model import BaseCSVModel
from models.embargo import Embargo


class EmbargoModel(BaseCSVModel[Embargo]):
    def __init__(self, file_path: str):
        super().__init__(file_path, Embargo)
