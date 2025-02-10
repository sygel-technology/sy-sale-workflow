# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends("route_id")
    def _compute_margin(self):
        res = super()._compute_margin()
        for line in self.filtered(
            lambda li: (
                li.route_id.deposit_operation
                and li.route_id.deposit_operation_type == "delivery_deposit"
            )
        ):
            line.margin = line.margin_percent = 0
        return res
