# Copyright 2023 Angel Garcia de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    use_confirmed_prefix = fields.Boolean(
        string="Different Prefix for Confirmed Sale Orders",
        related="company_id.use_confirmed_prefix",
        store=True,
        readonly=False,
    )
    confirmed_prefix = fields.Char(
        string="Confirmed Sale Order Prefix",
        related="company_id.confirmed_prefix",
        store=True,
        readonly=False,
    )
