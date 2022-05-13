# Copyright 2022 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def get_sale_order_line_multiline_description_sale(self, product):
        super(SaleOrderLine, self).get_sale_order_line_multiline_description_sale(product)
        return_val = product.with_context(display_default_code=True).display_name
        return return_val
