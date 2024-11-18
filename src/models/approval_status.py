# models/approval_status.py

from enum import Enum


class ApprovalStatus(str, Enum):
    PENDIENTE = "Pendiente"
    APROBADO = "Aprobado"
    RECHAZADO = "Rechazado"
