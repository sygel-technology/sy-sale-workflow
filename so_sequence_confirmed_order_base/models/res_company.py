# Copyright 2023 Angel Garcia de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    use_confirmed_prefix = fields.Boolean(
        string="Different Prefix for Confirmed Sale Orders",
        default=False
    )
    confirmed_prefix = fields.Char(
        string='Confirmed Sale Order Prefix',
    )
