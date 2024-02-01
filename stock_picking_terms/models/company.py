# Copyright 2024 Angel Garcia de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    stock_picking_terms = fields.Html(
        string="Terms and Conditions Stock Picking",
        translate=True
    )
