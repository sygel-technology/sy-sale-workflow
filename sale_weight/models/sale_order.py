# Copyright 2020 Valentin Vinagre <valentin.vinagre@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    total_weight = fields.Float(
        string='Total Weight',
        compute='_compute_total_weight',
        digits='Stock Weight',
        store=True,
        compute_sudo=True
    )

    @api.depends('order_line.weight')
    def _compute_total_weight(self):
        for sel in self:
            sel.total_weight = sum(sel.order_line.filtered('product_id').mapped('weight'))
