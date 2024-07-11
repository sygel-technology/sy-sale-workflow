# Copyright 2024 Ángel García de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class Product(models.Model):
    _inherit = "product.product"

    def get_product_multiline_description_sale(self):
        if self.env.context.get("no_internal_ref", False) and self.default_code:
            name = self.display_name.replace(f"[{self.default_code}] ", "")
            if self.description_sale:
                name += "\n" + self.description_sale
        else:
            name = super().get_product_multiline_description_sale()
        return name
