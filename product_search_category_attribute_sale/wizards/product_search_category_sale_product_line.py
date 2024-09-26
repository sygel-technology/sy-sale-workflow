# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductSearchCatSaleProductLine(models.TransientModel):
    _name = "product.search.cat.sale.product.line"
    _description = "Product Search Category Sale Product Line"

    product_search_cat_attr_sale_id = fields.Many2one(
        comodel_name="product.search.cat.attr.sale"
    )
    product_id = fields.Many2one(comodel_name="product.product", string="Product")
    attribute_value_ids = fields.Many2many(
        comodel_name="product.attribute.value",
        compute="_compute_attribute_value_ids",
        string="Attributes",
    )
    quantity = fields.Float()

    @api.depends("product_id")
    def _compute_attribute_value_ids(self):
        for sel in self:
            if sel.product_id.attribute_line_ids:
                attribute_value_ids = sel.product_id.attribute_line_ids.mapped(
                    "value_ids"
                ).ids
            else:
                attribute_value_ids = False
            sel.attribute_value_ids = attribute_value_ids

    def get_sale_order_vals(self, sale):
        self.ensure_one()
        return {
            "order_id": sale.id,
            "product_id": self.product_id.id,
            "product_uom_qty": self.quantity,
        }
