# Copyright 2020 Valentin Vinagre <valentin.vinagre@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def _get_sale_conditions(self):
        sale_conditions = False
        sale_conditions = self.env['sale.order.condition'].search([
            ('company_id', '=', self.env.user.company_id.id),
            ('default', '=', True)
        ], limit=1)
        return sale_conditions

    sale_conditions = fields.Many2one(
        'sale.order.condition',
        string='Sale Conditions',
        default=_get_sale_conditions
    )
