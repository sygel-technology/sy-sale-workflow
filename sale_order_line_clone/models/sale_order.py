# Copyright 2024 Roger Sans <roger.sans@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    can_clone_sale_line = fields.Boolean(
        string="Can Clone Sale Order Line",
        default=True,
        compute="_compute_product_sale_line",
        store=True,
        readonly=False,
    )

    @api.depends("product_id", "product_id.can_clone_sale_line")
    def _compute_product_sale_line(self):
        for record in self:
            if record.product_id:
                prod_can_clone_sale_line = record.product_id.can_clone_sale_line
                record.can_clone_sale_line = prod_can_clone_sale_line
        return False

    def copy(self, default=None):
        default = dict(default or {})
        default.update(
            {
                "order_id": self.order_id.id,
            }
        )
        return super().copy(default)
