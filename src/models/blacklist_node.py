# models/blacklist_node.py

from typing import Optional
from models.cotizante import Cotizante


class BlacklistNode:
    def __init__(self, cotizante: Cotizante):
        self.cotizante = cotizante
        self.next: Optional['BlacklistNode'] = None
