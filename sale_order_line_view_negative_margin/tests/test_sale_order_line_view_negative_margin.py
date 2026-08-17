# Copyright 2026 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestSaleOrderLineViewNegativeMargin(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Partner",
            }
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "list_price": 15.0,
                "standard_price": 10.0,
            }
        )
        cls.sale = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner.id,
            }
        )
        cls.line = cls.env["sale.order.line"].create(
            {
                "order_id": cls.sale.id,
                "product_id": cls.product.id,
                "product_uom_qty": 1.0,
                "price_unit": 15.0,
            }
        )

    def test_positive_margin(self):
        self.assertFalse(self.line.negative_margin)

    def test_negative_margin(self):
        self.line.price_unit = 8.0
        self.assertTrue(self.line.negative_margin)

    def test_zero_margin(self):
        self.line.price_unit = 10.0
        self.assertTrue(self.line.negative_margin)

    def test_negative_margin_with_quantity(self):
        self.line.write(
            {
                "product_uom_qty": 3.0,
                "price_unit": 9.0,
            }
        )
        self.assertTrue(self.line.negative_margin)

    def test_margin_becomes_positive(self):
        self.line.price_unit = 8.0
        self.assertTrue(self.line.negative_margin)
        self.line.price_unit = 15.0
        self.assertFalse(self.line.negative_margin)
