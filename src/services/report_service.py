# servicios/report_service.py

from models.transfer_request_model import TransferRequestModel
from models.embargo_model import EmbargoModel
from models.cotizante_model import CotizanteModel
from typing import List
import csv

class ReportService:
    """
    Servicio encargado de generar informes sobre las transferencias y embargos.
    """

    def __init__(
        self,
        transfer_request_model: TransferRequestModel,
        embargo_model: EmbargoModel,
        cotizante_model: CotizanteModel,
    ):
        self.transfer_request_model = transfer_request_model
        self.embargo_model = embargo_model
        self.cotizante_model = cotizante_model

    def generar_reporte_transferencias(self, output_file: str):
        """
        Genera un informe de todas las transferencias.

        Args:
            output_file (str): Ruta del archivo de salida.
        """
        transfer_requests = self.transfer_request_model.leer_todas_las_filas()
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["ID Transferencia", "ID Cotizante", "Estado Aprobación"])
            for transfer in transfer_requests:
                writer.writerow([transfer.id_transfer, transfer.id_cotizante, transfer.estado_aprobacion])
        print(f"Reporte de transferencias generado en {output_file}")

    def generar_reporte_embargos(self, output_file: str):
        """
        Genera un informe de todos los embargos.

        Args:
            output_file (str): Ruta del archivo de salida.
        """
        embargos = self.embargo_model.leer_todas_las_filas()
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["ID Embargo", "ID Cotizante", "Fecha", "Monto"])
            for embargo in embargos:
                writer.writerow([embargo.id_embargo, embargo.id_cotizante, embargo.fecha, embargo.monto])
        print(f"Reporte de embargos generado en {output_file}")
