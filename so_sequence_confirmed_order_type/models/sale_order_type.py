# Copyright 2023 Ángel García de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleOrderTypology(models.Model):
    _inherit = "sale.order.type"

    use_confirmed_so_prefix_by_type = fields.Boolean(
        string="Different Prefix for Confirmed Sale Orders",
    )
    confirmed_so_prefix_by_type = fields.Char(
        string='Confirmed Sale Order Prefix',
    )
