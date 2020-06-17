# Copyright 2020 Valentin Vinagre <valentin.vinagre@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    weight = fields.Float(
        string='Weight',
        compute='_compute_weight',
        digits='Stock Weight',
        store=True,
        compute_sudo=True
    )

    @api.depends('product_id', 'product_uom_qty')
    def _compute_weight(self):
        for line in self:
            weight = 0.0
            if line.product_id:
                weight = line.product_id.weight * line.product_uom_qty
            line.weight = weight
