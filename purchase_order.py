"""Modelos del dominio para la aprobación de órdenes de compra."""

from dataclasses import dataclass


@dataclass
class Supplier:
    """Representa un proveedor y su presupuesto disponible."""

    supplier_id: int
    name: str
    available_budget: float


@dataclass
class PurchaseOrder:
    """Representa una orden de compra."""

    order_id: int
    supplier_id: int
    amount: float
    status: str = "PENDING"

    def __post_init__(self):
        if self.amount <= 0:
            raise ValueError("El monto de la orden debe ser mayor que cero.")
