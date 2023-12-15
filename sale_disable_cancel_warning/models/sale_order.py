# Copyright 2023 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_cancel(self):
        if self.env['ir.config_parameter'].sudo().get_param(
            'sale_disable_cancel_warning.disable_cancel_warning'
        ):
            self = self.with_context(disable_cancel_warning=True)
        return super().action_cancel()
