# models/priority_transfer_queue.py

import heapq
from typing import Optional
from models.transfer_request import TransferRequest


class PriorityTransferQueue:
    def __init__(self):
        self.heap = []

    def agregar_transferencia(self, transfer: TransferRequest, prioridad: int):
        heapq.heappush(self.heap, (prioridad, transfer))

    def obtener_siguiente_transferencia(self) -> Optional[TransferRequest]:
        if self.heap:
            return heapq.heappop(self.heap)[1]
        return None

    def es_vacia(self) -> bool:
        return len(self.heap) == 0
