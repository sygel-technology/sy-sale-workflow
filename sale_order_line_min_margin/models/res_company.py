# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    apply_so_line_min_margin = fields.Boolean(
        string="Apply Sale Order Line Min. Margin"
    )
    so_line_min_margin = fields.Float(
        string="Sale Order Line Min. Margin (%)",
        digits="Product Price",
    )
