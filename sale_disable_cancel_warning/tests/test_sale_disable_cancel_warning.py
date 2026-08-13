# Copyright 2026 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestSaleCancelWarning(TransactionCase):
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
                "type": "consu",
                "list_price": 100.0,
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

    def test_disable_cancel_warning_default(self):
        self.assertTrue(self.env.company.disable_cancel_warning)

    def test_disable_cancel_warning_config_settings(self):
        settings = self.env["res.config.settings"].create(
            {
                "disable_cancel_warning": False,
            }
        )

        settings.execute()
        self.assertFalse(self.env.company.disable_cancel_warning)

    def test_cancel_with_warning_disabled(self):
        self.env.company.disable_cancel_warning = True
        sale = self._create_sale_order()
        sale.action_confirm()
        sale.action_cancel()
        self.assertEqual(sale.state, "cancel")

    def test_cancel_with_warning_enabled(self):
        self.env.company.disable_cancel_warning = False
        sale = self._create_sale_order()
        sale.action_confirm()
        result = sale.action_cancel()
        self.assertEqual(result.get("res_model"), "sale.order.cancel")
