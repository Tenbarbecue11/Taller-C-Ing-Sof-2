"""Pruebas unitarias del servicio de aprobación con unittest y Mock."""

import unittest
from unittest.mock import Mock

from exceptions import (
    AlreadyApprovedError,
    InsufficientBudgetError,
)
from purchase_order import PurchaseOrder, Supplier
from purchase_order_service import PurchaseOrderService


class TestPurchaseOrderService(unittest.TestCase):
    """Prueba los escenarios principales de aprobación."""

    def setUp(self):
        self.order_repository = Mock()
        self.supplier_repository = Mock()
        self.service = PurchaseOrderService(
            self.order_repository,
            self.supplier_repository,
        )
        self.order = PurchaseOrder(
            order_id=101,
            supplier_id=7,
            amount=300.0,
        )
        self.supplier = Supplier(
            supplier_id=7,
            name="Proveedor de prueba",
            available_budget=1000.0,
        )
        self.order_repository.get_by_id.return_value = self.order
        self.supplier_repository.get_by_id.return_value = self.supplier

    def test_approve_order_successfully_and_deduct_budget(self):
        """Una orden válida se aprueba y descuenta el presupuesto."""
        result = self.service.approve(101)

        self.assertEqual(result.status, "APPROVED")
        self.assertEqual(self.supplier.available_budget, 700.0)
        self.supplier_repository.save.assert_called_once_with(self.supplier)
        self.order_repository.save.assert_called_once_with(self.order)

    def test_reject_order_when_budget_is_insufficient(self):
        """No se aprueba ni se guarda una orden que supera el presupuesto."""
        self.supplier.available_budget = 200.0

        with self.assertRaises(InsufficientBudgetError):
            self.service.approve(101)

        self.assertEqual(self.order.status, "PENDING")
        self.assertEqual(self.supplier.available_budget, 200.0)
        self.supplier_repository.save.assert_not_called()
        self.order_repository.save.assert_not_called()

    def test_reject_order_that_was_already_approved(self):
        """Una orden aprobada no puede aprobarse una segunda vez."""
        self.order.status = "APPROVED"

        with self.assertRaises(AlreadyApprovedError):
            self.service.approve(101)

        self.supplier_repository.get_by_id.assert_not_called()
        self.supplier_repository.save.assert_not_called()
        self.order_repository.save.assert_not_called()


if __name__ == "__main__":
    unittest.main()
