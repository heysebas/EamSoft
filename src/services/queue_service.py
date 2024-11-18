# servicios/queue_service.py

from models.priority_transfer_queue import PriorityTransferQueue
from models.transfer_request import TransferRequest
from typing import Optional

class QueueService:
    """
    Servicio encargado de gestionar la cola de prioridades para las transferencias.
    """

    def __init__(self):
        self.priority_queue = PriorityTransferQueue()

    def agregar_a_cola(self, transfer_request: TransferRequest, prioridad: int):
        """
        Agrega una solicitud de transferencia a la cola con una prioridad específica.

        Args:
            transfer_request (TransferRequest): La solicitud de transferencia.
            prioridad (int): La prioridad de la transferencia.
        """
        self.priority_queue.agregar_transferencia(transfer_request, prioridad)

    def obtener_siguiente_transferencia(self) -> Optional[TransferRequest]:
        """
        Obtiene la siguiente transferencia en la cola según la prioridad.

        Returns:
            Optional[TransferRequest]: La siguiente solicitud de transferencia o None si la cola está vacía.
        """
        return self.priority_queue.obtener_siguiente_transferencia()

    def es_vacia(self) -> bool:
        """
        Verifica si la cola está vacía.

        Returns:
            bool: True si la cola está vacía, False en caso contrario.
        """
        return self.priority_queue.es_vacia()
