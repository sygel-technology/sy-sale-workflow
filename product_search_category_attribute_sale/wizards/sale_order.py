# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_open_product_search_cat_attr_sale(self):
        self.ensure_one()
        view_id = self.env.ref(
            "product_search_category_attribute_sale.product_search_cat_attr_sale_form_view"
        )
        ctx = {
            "default_sale_id": self.id,
        }
        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "product.search.cat.attr.sale",
            "target": "new",
            "view_id": view_id.id,
            "context": ctx,
        }
