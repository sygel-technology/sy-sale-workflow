# Copyright 2024 Angel Garcia de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    stock_picking_terms = fields.Html(
        string="Terms and Conditions Stock Picking",
        related="company_id.stock_picking_terms",
        readonly=False
    )
