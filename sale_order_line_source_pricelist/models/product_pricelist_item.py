# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    def get_recursive_item_id(self, product, quantity, uom, date):
        """Returns the final source pricelist items for recursive ones"""
        self.ensure_one()
        res = self
        if self.base == "pricelist" and self.base_pricelist_id:
            next_item = self.env["product.pricelist.item"].browse(
                self.base_pricelist_id._get_product_rule(
                    product, quantity=quantity, uom=uom, date=date
                )
            )
            if next_item:
                res = next_item.get_recursive_item_id(product, quantity, uom, date)
        return res
