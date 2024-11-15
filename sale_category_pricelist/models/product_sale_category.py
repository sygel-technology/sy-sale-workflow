# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductSaleCategory(models.Model):
    _name = "product.sale.category"
    _description = "Product Sale Category"
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = "complete_name"
    _order = "complete_name"

    name = fields.Char(index="trigram", required=True)
    complete_name = fields.Char(
        compute="_compute_complete_name", recursive=True, store=True
    )
    parent_id = fields.Many2one(
        "product.sale.category", "Parent Category", index=True, ondelete="cascade"
    )
    parent_path = fields.Char(index=True, unaccent=False)
    child_id = fields.One2many("product.sale.category", "parent_id", "Child Categories")
    product_count = fields.Integer(
        "# Products",
        compute="_compute_product_count",
        help="The number of products under this category"
        "(Does not consider the children categories)",
    )

    @api.depends("name", "parent_id.complete_name")
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = "{} / {}".format(
                    category.parent_id.complete_name,
                    category.name,
                )
            else:
                category.complete_name = category.name

    def _compute_product_count(self):
        read_group_res = self.env["product.template"].read_group(
            [("sale_categ_id", "child_of", self.ids)],
            ["sale_categ_id"],
            ["sale_categ_id"],
        )
        group_data = dict(
            (data["sale_categ_id"][0], data["sale_categ_id_count"])
            for data in read_group_res
        )
        for categ in self:
            product_count = 0
            for sub_categ_id in categ.search([("id", "child_of", categ.ids)]).ids:
                product_count += group_data.get(sub_categ_id, 0)
            categ.product_count = product_count

    @api.constrains("parent_id")
    def _check_category_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_("You cannot create recursive categories."))

    @api.model
    def name_create(self, name):
        return self.create({"name": name}).name_get()[0]

    def name_get(self):
        if not self.env.context.get("hierarchical_naming", True):
            return [(record.id, record.name) for record in self]
        return super().name_get()
