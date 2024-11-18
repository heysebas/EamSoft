# servicios/embargo_service.py

from models.embargo_model import EmbargoModel
from models.cotizante_model import CotizanteModel
from typing import List

class EmbargoService:
    """
    Servicio encargado de gestionar los embargos de los cotizantes.
    """

    def __init__(self, embargo_model: EmbargoModel):
        self.embargo_model = embargo_model

    def verificar_embargo(self, id_cotizante: str) -> bool:
        """
        Verifica si un cotizante está sujeto a embargo.

        Args:
            id_cotizante (str): El ID del cotizante.

        Returns:
            bool: True si está sujeto a embargo, False en caso contrario.
        """
        embargos = self.embargo_model.leer_todas_las_filas()
        for embargo in embargos:
            if embargo.id_cotizante == id_cotizante:
                return True
        return False

    def obtener_embargos_por_cotizante(self, id_cotizante: str) -> List:
        """
        Obtiene todos los embargos asociados a un cotizante.

        Args:
            id_cotizante (str): El ID del cotizante.

        Returns:
            List: Lista de embargos.
        """
        embargos = self.embargo_model.leer_todas_las_filas()
        return [embargo for embargo in embargos if embargo.id_cotizante == id_cotizante]
