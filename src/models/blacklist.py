# models/blacklist.py

from typing import Iterator
from models.blacklist_node import BlacklistNode
from models.cotizante import Cotizante


class Blacklist:
    def __init__(self):
        self.head: Optional[BlacklistNode] = None

    def agregar(self, cotizante: Cotizante):
        new_node = BlacklistNode(cotizante)
        new_node.next = self.head
        self.head = new_node

    def iterar_embargables(self) -> Iterator[Cotizante]:
        current = self.head
        while current:
            yield current.cotizante
            current = current.next

    def buscar(self, id_cotizante: str) -> bool:
        current = self.head
        while current:
            if current.cotizante.id_cotizante == id_cotizante:
                return True
            current = current.next
        return False
