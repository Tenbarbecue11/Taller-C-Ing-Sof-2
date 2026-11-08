"""Servicio que contiene las reglas de aprobación de órdenes de compra."""

from exceptions import (
    AlreadyApprovedError,
    InsufficientBudgetError,
    PurchaseOrderNotFoundError,
    SupplierNotFoundError,
)


class PurchaseOrderService:
    """Coordina la aprobación de órdenes usando repositorios inyectados."""

    def __init__(self, order_repository, supplier_repository):
        self.order_repository = order_repository
        self.supplier_repository = supplier_repository

    def approve(self, order_id):
        """Aprueba una orden, descuenta el presupuesto y persiste los cambios.

        El método espera que los repositorios implementen:
        - order_repository.get_by_id(order_id)
        - order_repository.save(order)
        - supplier_repository.get_by_id(supplier_id)
        - supplier_repository.save(supplier)
        """
        order = self.order_repository.get_by_id(order_id)
        if order is None:
            raise PurchaseOrderNotFoundError(
                f"No existe la orden de compra {order_id}."
            )

        if order.status == "APPROVED":
            raise AlreadyApprovedError(
                f"La orden {order_id} ya fue aprobada."
            )

        supplier = self.supplier_repository.get_by_id(order.supplier_id)
        if supplier is None:
            raise SupplierNotFoundError(
                f"No existe el proveedor {order.supplier_id}."
            )

        if order.amount > supplier.available_budget:
            raise InsufficientBudgetError(
                "El presupuesto disponible del proveedor es insuficiente."
            )

        # Solo se modifican y guardan los objetos después de validar las reglas.
        supplier.available_budget -= order.amount
        order.status = "APPROVED"

        self.supplier_repository.save(supplier)
        self.order_repository.save(order)

        return order
