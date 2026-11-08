"""Excepciones de negocio para la aprobación de órdenes de compra."""


class PurchaseOrderError(Exception):
    """Error base del proceso de aprobación."""


class PurchaseOrderNotFoundError(PurchaseOrderError):
    """La orden solicitada no existe."""


class SupplierNotFoundError(PurchaseOrderError):
    """El proveedor asociado no existe."""


class InsufficientBudgetError(PurchaseOrderError):
    """El proveedor no tiene presupuesto suficiente."""


class AlreadyApprovedError(PurchaseOrderError):
    """La orden ya fue aprobada anteriormente."""
