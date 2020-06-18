# Copyright 2020 Valentin Vinagre <valentin.vinagre@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    price_discount = fields.Float(
        digits='Discount'
    )
    percent_price = fields.Float(
        digits='Discount'
    )
