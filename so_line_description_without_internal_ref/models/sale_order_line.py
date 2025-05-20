# Copyright 2024 Ángel García de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def get_sale_order_line_multiline_description_sale(self, product):
        return (
            product.with_context(
                no_internal_ref=True
            ).get_product_multiline_description_sale()
            + self._get_sale_order_line_multiline_description_variants()
        )
