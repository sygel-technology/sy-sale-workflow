# Copyright 2026 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.sale_stock_deposit.tests.test_sale_stock_deposit import (
    TestSaleStockDeposit,
)


class SomethingCase(TestSaleStockDeposit):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product.write(
            {
                "lst_price": 10,
                "standard_price": 1,
            }
        )

    def test_sale_stock_deposit_margin(self):
        self.create_deposit(self.partner, self.main_deposit_location)
        order1 = self.create_deposit_sale("deposit")
        order1._compute_margin()
        self.assertTrue(order1.order_line.margin)
        self.assertTrue(order1.order_line.margin_percent)
        order2 = self.create_deposit_sale("delivery_deposit")
        order2._compute_margin()
        self.assertFalse(order2.order_line.margin)
        self.assertFalse(order2.order_line.margin_percent)
