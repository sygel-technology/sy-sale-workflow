# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    apply_so_line_min_margin = fields.Boolean(
        string="Apply Sale Order Line Min. Margin",
        related="company_id.apply_so_line_min_margin",
        readonly=False,
    )
    so_line_min_margin = fields.Float(
        string="Sale Order Line Min. Margin (%)",
        related="company_id.so_line_min_margin",
        digits="Product Price",
        readonly=False,
    )
