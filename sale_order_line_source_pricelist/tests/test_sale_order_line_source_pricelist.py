# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestSaleLinePricelistItem(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.pricelist1 = cls.env["product.pricelist"].create(
            {
                "name": "Test pricelist 1",
            }
        )
        cls.pl_item_1 = cls.env["product.pricelist.item"].create(
            {
                "pricelist_id": cls.pricelist1.id,
                "applied_on": "3_global",
                "compute_price": "fixed",
                "fixed_price": "100",
            },
        )
        cls.pricelist2 = cls.env["product.pricelist"].create(
            {
                "name": "Test pricelist 2",
            }
        )
        cls.pl_item_2 = cls.env["product.pricelist.item"].create(
            {
                "pricelist_id": cls.pricelist2.id,
                "applied_on": "3_global",
                "compute_price": "formula",
                "base": "pricelist",
                "base_pricelist_id": cls.pricelist1.id,
                "price_discount": 90,
            },
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Partner",
                "property_product_pricelist": cls.pricelist2.id,
            }
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
            }
        )

    def test(self):
        so = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
            }
        )
        so_line = self.env["sale.order.line"].create(
            {
                "order_id": so.id,
                "product_id": self.product.id,
                "product_uom_qty": 1,
            }
        )
        self.assertEqual(so.pricelist_id, self.pricelist2)
        self.assertEqual(so_line.pricelist_item_id, self.pl_item_2)
        self.assertEqual(so_line.source_pricelist_item_id, self.pl_item_1)
        self.assertEqual(so_line.source_pricelist_id, self.pricelist1)
        self.assertEqual(so_line.price_unit, 10)
