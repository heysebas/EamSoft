# servicios/transfer_service.py

from models.cotizante_model import CotizanteModel
from models.transfer_request_model import TransferRequestModel
from services.validation_service import ValidationService
from services.embargo_service import EmbargoService
from services.queue_service import QueueService
from services.blacklist_service import BlacklistService
from models.approval_status import ApprovalStatus
from models.transfer_request import TransferRequest
from models.cotizante import Cotizante
from typing import Optional

class TransferService:
    """
    Servicio encargado de orquestar el proceso de transferencias de cotizantes.
    """

    def __init__(
        self,
        cotizante_model: CotizanteModel,
        transfer_request_model: TransferRequestModel,
        embargo_service: EmbargoService,
        validation_service: ValidationService,
        queue_service: QueueService,
        blacklist_service: BlacklistService,
    ):
        self.cotizante_model = cotizante_model
        self.transfer_request_model = transfer_request_model
        self.embargo_service = embargo_service
        self.validation_service = validation_service
        self.queue_service = queue_service
        self.blacklist_service = blacklist_service

    def procesar_transferencias(self):
        """
        Procesa todas las solicitudes de transferencia.
        """
        transfer_requests = self.transfer_request_model.leer_todas_las_filas()
        cotizantes = {c.id_cotizante: c for c in self.cotizante_model.leer_todas_las_filas()}

        for transfer in transfer_requests:
            cotizante = cotizantes.get(transfer.id_cotizante)
            if not cotizante:
                print(f"Cotizante con ID {transfer.id_cotizante} no encontrado.")
                continue

            # Validar la solicitud de transferencia
            valido, mensaje = self.validation_service.validar_transferencia(transfer, cotizante)
            if not valido:
                print(f"Transferencia {transfer.id_transfer} inválida: {mensaje}")
                continue

            # Verificar embargo
            embargo = self.embargo_service.verificar_embargo(cotizante.id_cotizante)
            if embargo:
                self.blacklist_service.agregar_a_lista_negra(cotizante)
                transfer.estado_aprobacion = ApprovalStatus.RECHAZADO.value
                print(f"Transferencia {transfer.id_transfer} rechazada por embargo.")
            else:
                transfer.estado_aprobacion = ApprovalStatus.APROBADO.value
                # Asignar prioridad (por ejemplo, basado en la fecha de solicitud)
                prioridad = self.determinar_prioridad(cotizante)
                self.queue_service.agregar_a_cola(transfer, prioridad)
                print(f"Transferencia {transfer.id_transfer} aprobada y agregada a la cola.")

        # Actualizar el estado de las transferencias en el modelo
        self.actualizar_estados_transferencias(transfer_requests)

        # Ejecutar la cola de transferencias
        self.ejecutar_cola()

    def determinar_prioridad(self, cotizante: Cotizante) -> int:
        """
        Determina la prioridad de una transferencia.

        Args:
            cotizante (Cotizante): El cotizante a transferir.

        Returns:
            int: La prioridad asignada (más bajo es mayor prioridad).
        """
        # Implementar lógica de prioridad, por ejemplo, antigüedad
        # Por ahora, retornamos una prioridad estática
        return 1

    def actualizar_estados_transferencias(self, transfer_requests):
        """
        Actualiza el estado de las transferencias en el modelo.

        Args:
            transfer_requests (List[TransferRequest]): Lista de solicitudes de transferencia.
        """
        for transfer in transfer_requests:
            self.transfer_request_model.escribir_fila(transfer)

    def ejecutar_cola(self):
        """
        Procesa todas las transferencias en la cola de prioridad.
        """
        while not self.queue_service.es_vacia():
            transfer = self.queue_service.obtener_siguiente_transferencia()
            self.procesar_transferencia(transfer)

    def procesar_transferencia(self, transfer: TransferRequest):
        """
        Procesa una única transferencia.

        Args:
            transfer (TransferRequest): La solicitud de transferencia a procesar.
        """
        # Implementar la lógica para procesar la transferencia
        # Esto podría incluir actualizar registros en el sistema de Colpensionex
        print(f"Procesando transferencia: {transfer.id_transfer} para cotizante {transfer.id_cotizante}")
        # Aquí se podría agregar código para actualizar la base de datos, generar archivos de salida, etc.
