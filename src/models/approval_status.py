# models/approval_status.py

# Import the Enum base class for creating enumerations
from enum import Enum

# Define the ApprovalStatus class
# This is an enumeration to represent the status of an approval process.
# It inherits from both `str` and `Enum` to allow the enumeration values to be treated as strings.
class ApprovalStatus(str, Enum):
    # Enumeration members with their corresponding string values.
    PENDIENTE = "Pendiente"  # The request is pending review.
    APROBADO = "Aprobado"    # The request has been approved.
    RECHAZADO = "Rechazado"  # The request has been rejected.