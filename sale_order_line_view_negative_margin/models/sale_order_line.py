# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools import float_compare


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    negative_margin = fields.Boolean(compute="_compute_negative_margin")

    @api.depends("price_subtotal", "product_uom_qty", "purchase_price")
    def _compute_negative_margin(self):
        dp_product_price = self.env["decimal.precision"].precision_get("Product Price")
        for line in self:
            line.negative_margin = (
                float_compare(
                    line.price_subtotal
                    - (line.sudo().purchase_price * line.product_uom_qty),
                    0.0,
                    precision_digits=dp_product_price,
                )
                <= 0
            )
