# servicios/validation_service.py

from models.transfer_request import TransferRequest
from models.cotizante import Cotizante
from models.approval_status import ApprovalStatus
from typing import Tuple

class ValidationService:
    """
    Servicio encargado de validar las solicitudes de transferencia de cotizantes.
    """

    def validar_transferencia(self, transfer_request: TransferRequest, cotizante: Cotizante) -> Tuple[bool, str]:
        """
        Valida si una solicitud de transferencia es válida.

        Args:
            transfer_request (TransferRequest): La solicitud de transferencia.
            cotizante (Cotizante): El cotizante asociado a la solicitud.

        Returns:
            Tuple[bool, str]: Un booleano indicando si la validación fue exitosa y un mensaje.
        """
        # Ejemplo de validaciones
        if not cotizante.desea_transferir:
            return False, "El cotizante no desea transferir su pensión."

        if cotizante.fondo_actual.lower() == "colpensionex":
            return False, "El cotizante ya está en el fondo Colpensionex."

        # Validar formato de datos
        if not cotizante.id_cotizante.strip():
            return False, "ID de cotizante vacío."

        # Otras validaciones según requisitos

        return True, "Validación exitosa."
