# Copyright 2021 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _compute_amount_untaxed_without_delivery(self):
        self.ensure_one()
        delivery_cost_untaxed = sum([l.price_subtotal for l in self.order_line if l.is_delivery])
        return float(self.amount_untaxed) - delivery_cost_untaxed
