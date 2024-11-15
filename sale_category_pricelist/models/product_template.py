# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    sale_categ_id = fields.Many2one(
        comodel_name="product.sale.category",
        string="Product Sale Category",
    )
