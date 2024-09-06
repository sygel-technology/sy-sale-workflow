# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductSearchCatAttrLineSale(models.TransientModel):
    _name = "product.search.cat.attr.line.sale"
    _inherit = "product.search.cat.attr.line"
    _description = "Product Search Cat Attr Line Sale"

    search_id = fields.Many2one(comodel_name="product.search.cat.attr.sale")
