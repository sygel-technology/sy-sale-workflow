# Copyright 2025 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestSaleAdvancePaymentInv(TransactionCase):
    def test_default_get_consolidated_billing(self):
        defaults = self.env["sale.advance.payment.inv"].default_get(
            ["consolidated_billing"]
        )
        self.assertIn(
            "consolidated_billing",
            defaults,
            "Field consolidated_billing should be in defaults",
        )
        self.assertFalse(
            defaults["consolidated_billing"],
            "Default value of consolidated_billing should be False",
        )
