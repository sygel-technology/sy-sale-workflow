# Copyright 2026 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields
from odoo.tests import TransactionCase


class TestSaleOrderTypeConfirmReason(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.company = cls.env.company
        cls.company.sale_confirm_reason = True

        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Customer",
            }
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "list_price": 100.0,
            }
        )
        cls.order_type_with_reason = cls.env["sale.order.type"].create(
            {
                "name": "Type With Confirmation Reason",
                "require_confirm_reason": True,
            }
        )
        cls.order_type_without_reason = cls.env["sale.order.type"].create(
            {
                "name": "Type Without Confirmation Reason",
                "require_confirm_reason": False,
            }
        )

    def _create_sale_order(self, order_type):
        return self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "type_id": order_type.id,
                "order_line": [
                    fields.Command.create(
                        {
                            "product_id": self.product.id,
                            "product_uom_qty": 1.0,
                            "price_unit": 100.0,
                        }
                    )
                ],
            }
        )

    def test_confirm_reason_required(self):
        order = self._create_sale_order(self.order_type_with_reason)
        result = order.action_confirm()
        self.assertEqual(
            result["res_model"],
            "sale.confirm.reason.wizard",
        )
        self.assertEqual(
            result["context"]["default_order_ids"],
            [fields.Command.set(order.ids)],
        )
        self.assertEqual(order.state, "draft")

    def test_confirm_reason_not_required(self):
        order = self._create_sale_order(self.order_type_without_reason)
        result = order.action_confirm()
        self.assertTrue(result)
        self.assertEqual(order.state, "sale")

    def test_requires_confirm_reason(self):
        order_with_reason = self._create_sale_order(self.order_type_with_reason)
        order_without_reason = self._create_sale_order(self.order_type_without_reason)
        self.assertTrue(order_with_reason._show_confirm_reason_wizard())
        self.assertFalse(order_without_reason._show_confirm_reason_wizard())

    def test_confirm_reason_disabled_on_company(self):
        self.company.sale_confirm_reason = False
        order = self._create_sale_order(self.order_type_with_reason)
        self.assertFalse(order._show_confirm_reason_wizard())
        result = order.action_confirm()
        self.assertTrue(result)
        self.assertEqual(order.state, "sale")

    def test_mass_confirm_reason_required(self):
        order_with_reason = self._create_sale_order(self.order_type_with_reason)
        order_without_reason = self._create_sale_order(self.order_type_without_reason)
        orders = order_with_reason | order_without_reason
        result = orders.action_confirm()
        self.assertEqual(
            result["res_model"],
            "sale.confirm.reason.wizard",
        )
        self.assertEqual(
            result["context"]["default_order_ids"],
            [fields.Command.set(orders.ids)],
        )
        self.assertTrue(all(order.state == "draft" for order in orders))

    def test_mass_confirm_reason_not_required(self):
        orders = self._create_sale_order(
            self.order_type_without_reason
        ) | self._create_sale_order(self.order_type_without_reason)
        orders.action_confirm()
        self.assertTrue(all(order.state == "sale" for order in orders))
