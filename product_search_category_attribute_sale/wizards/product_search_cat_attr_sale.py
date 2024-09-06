# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductSearchCatAttrSale(models.TransientModel):
    _name = "product.search.cat.attr.sale"
    _inherit = "product.search.cat.attr"
    _description = "Product Search Cat Attr Sale"

    RELOAD_VIEW = (
        "product_search_category_attribute_sale.product_search_cat_attr_sale_form_view"
    )

    attribute_line_ids = fields.One2many(
        comodel_name="product.search.cat.attr.line.sale",
    )
    product_line_ids = fields.One2many(
        comodel_name="product.search.cat.sale.product.line",
        inverse_name="product_search_cat_attr_sale_id",
    )
    sale_id = fields.Many2one(comodel_name="sale.order")

    def search_products(self):
        self.ensure_one()
        products = super()._search_products()
        prod_lines_to_create = []
        self.product_line_ids.unlink()
        for product in products:
            prod_lines_to_create.append(
                {"product_id": product.id, "product_search_cat_attr_sale_id": self.id}
            )
        if prod_lines_to_create:
            lines = self.env["product.search.cat.sale.product.line"].create(
                prod_lines_to_create
            )
            self.product_line_ids = lines.ids
        return super().reload_view()

    def create_order_lines(self):
        self.ensure_one()
        lines_to_create = []
        for line in self.product_line_ids.filtered(lambda a: a.quantity > 0):
            lines_to_create.append(line.get_sale_order_vals(self.sale_id))
        if lines_to_create:
            self.env["sale.order.line"].create(lines_to_create)

    def apply_category(self):
        return super().apply_category()

    def delete_category(self):
        self.product_line_ids.unlink()
        return super().delete_category()
