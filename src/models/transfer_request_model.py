# models/transfer_request_model.py

from models.base_csv_model import BaseCSVModel
from models.transfer_request import TransferRequest


class TransferRequestModel(BaseCSVModel[TransferRequest]):
    def __init__(self, file_path: str):
        super().__init__(file_path, TransferRequest)
