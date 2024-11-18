# servicios/blacklist_service.py

from models.blacklist import Blacklist
from models.cotizante import Cotizante

class BlacklistService:
    """
    Servicio encargado de gestionar la lista negra de cotizantes sujetos a embargo.
    """

    def __init__(self):
        self.blacklist = Blacklist()

    def agregar_a_lista_negra(self, cotizante: Cotizante):
        """
        Agrega un cotizante a la lista negra.

        Args:
            cotizante (Cotizante): El cotizante a agregar.
        """
        self.blacklist.agregar(cotizante)

    def esta_en_lista_negra(self, id_cotizante: str) -> bool:
        """
        Verifica si un cotizante está en la lista negra.

        Args:
            id_cotizante (str): El ID del cotizante.

        Returns:
            bool: True si está en la lista negra, False en caso contrario.
        """
        return self.blacklist.buscar(id_cotizante)

    def obtener_todos_embargables(self):
        """
        Obtiene todos los cotizantes sujetos a embargo en la lista negra.

        Returns:
            Iterator[Cotizante]: Un iterador sobre los cotizantes en la lista negra.
        """
        return self.blacklist.iterar_embargables()
