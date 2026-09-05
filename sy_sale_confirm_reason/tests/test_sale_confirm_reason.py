# Copyright 2026 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase


class TestSaleConfirmReason(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

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
        cls.reason = cls.env["sale.confirm.reason"].create(
            {
                "name": "Test Reason",
            }
        )
        cls.reason_with_text = cls.env["sale.confirm.reason"].create(
            {
                "name": "Reason With Text",
                "allow_manual_text": True,
            }
        )
        cls.reason_required_text = cls.env["sale.confirm.reason"].create(
            {
                "name": "Reason With Required Text",
                "allow_manual_text": True,
                "manual_text_required": True,
            }
        )

    def _create_sale_order(self):
        return self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "product_uom_qty": 1.0,
                            "price_unit": 100.0,
                        },
                    )
                ],
            }
        )

    def test_confirm_without_required_reason(self):
        order = self._create_sale_order()
        self.assertFalse(order._requires_confirm_reason())
        result = order.action_confirm()
        self.assertTrue(result)
        self.assertEqual(order.state, "sale")
        self.assertFalse(order.confirm_reason_id)

    def test_confirm_with_reason(self):
        order = self._create_sale_order()
        wizard = self.env["sale.confirm.reason.wizard"].create(
            {
                "order_id": order.id,
                "reason_id": self.reason.id,
            }
        )
        wizard.action_confirm()
        self.assertEqual(order.confirm_reason_id, self.reason)
        self.assertFalse(order.confirm_reason_details)
        self.assertEqual(order.state, "sale")

    def test_confirm_with_reason_details(self):
        order = self._create_sale_order()
        wizard = self.env["sale.confirm.reason.wizard"].create(
            {
                "order_id": order.id,
                "reason_id": self.reason_with_text.id,
                "details": "<p>Test details</p>",
            }
        )
        wizard.action_confirm()
        self.assertEqual(order.confirm_reason_id, self.reason_with_text)
        self.assertEqual(
            order.confirm_reason_details,
            "<p>Test details</p>",
        )
        self.assertEqual(order.state, "sale")

    def test_confirm_with_required_reason_details(self):
        order = self._create_sale_order()
        wizard = self.env["sale.confirm.reason.wizard"].create(
            {
                "order_id": order.id,
                "reason_id": self.reason_required_text.id,
                "details": "<p>Required details</p>",
            }
        )
        wizard.action_confirm()
        self.assertEqual(
            order.confirm_reason_id,
            self.reason_required_text,
        )
        self.assertEqual(
            order.confirm_reason_details,
            "<p>Required details</p>",
        )
        self.assertEqual(order.state, "sale")

    def test_details_not_stored_when_manual_text_not_allowed(self):
        order = self._create_sale_order()
        wizard = self.env["sale.confirm.reason.wizard"].create(
            {
                "order_id": order.id,
                "reason_id": self.reason.id,
                "details": "<p>This should not be stored</p>",
            }
        )
        wizard.action_confirm()
        self.assertEqual(order.confirm_reason_id, self.reason)
        self.assertFalse(order.confirm_reason_details)
        self.assertEqual(order.state, "sale")

    def test_copy_reason(self):
        copied_reason = self.reason.copy()
        self.assertEqual(
            copied_reason.name,
            "Test Reason (copy)",
        )
        self.assertNotEqual(
            copied_reason,
            self.reason,
        )

    def test_action_open_confirm_reason_wizard(self):
        order = self._create_sale_order()
        result = order._action_open_confirm_reason_wizard()
        self.assertEqual(
            result["type"],
            "ir.actions.act_window",
        )
        self.assertEqual(
            result["res_model"],
            "sale.confirm.reason.wizard",
        )
        self.assertEqual(
            result["view_mode"],
            "form",
        )
        self.assertEqual(
            result["target"],
            "new",
        )
        self.assertEqual(
            result["context"]["default_order_id"],
            order.id,
        )

    def test_onchange_reason_keeps_details_when_allowed(self):
        wizard = self.env["sale.confirm.reason.wizard"].new(
            {
                "reason_id": self.reason_with_text.id,
                "details": "<p>Test details</p>",
            }
        )
        wizard._onchange_reason_id()
        self.assertEqual(
            wizard.details,
            "<p>Test details</p>",
        )

    def test_onchange_reason_clears_details_when_not_allowed(self):
        wizard = self.env["sale.confirm.reason.wizard"].new(
            {
                "reason_id": self.reason.id,
                "details": "<p>Test details</p>",
            }
        )
        wizard._onchange_reason_id()
        self.assertFalse(wizard.details)
