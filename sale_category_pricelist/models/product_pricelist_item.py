# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    applied_on = fields.Selection(
        selection_add=[
            ("2_0_product_sale_category", "Product Sale Category"),
            ("1_product",),
            ("0_product_variant",),
        ],
        ondelete={
            "2_0_product_sale_category": "cascade",
        },
    )

    sale_categ_id = fields.Many2one(
        comodel_name="product.sale.category",
        string="Product Sale Category",
        ondelete="cascade",
        help="Specify a product sale category if this rule "
        "only applies to products belonging to this category "
        "or its children categories. Keep empty otherwise.",
    )

    @api.depends("applied_on", "sale_categ_id")
    def _compute_name_and_price(self):
        res = super()._compute_name_and_price()
        for item in self.filtered(
            lambda i: i.sale_categ_id and i.applied_on == "2_0_product_sale_category"
        ):
            item.name = _("Sale Category: {}").format(item.sale_categ_id.display_name)
        return res

    @api.constrains("sale_categ_id")
    def _check_product_consistency(self):
        res = super()._check_product_consistency()
        if self.filtered(
            lambda item: item.applied_on == "2_0_product_sale_category"
            and not item.sale_categ_id
        ):
            raise ValidationError(
                _(
                    "Please specify the sale category for which "
                    "this rule should be applied"
                )
            )
        return res

    def create(self, vals_list):
        for values in vals_list:
            if values.get("applied_on", False):
                # Ensure item consistency for later searches.
                applied_on = values["applied_on"]
                if applied_on in [
                    "3_global",
                    "2_product_category",
                    "1_product",
                    "0_product_variant",
                ]:
                    values.update(dict(sale_categ_id=None))
                elif applied_on == "2_0_product_sale_category":
                    values.update(
                        dict(product_id=None, product_tmpl_id=None, categ_id=None)
                    )
        return super().create(vals_list)

    def write(self, values):
        if values.get("applied_on", False):
            # Ensure item consistency for later searches.
            applied_on = values["applied_on"]
            if applied_on in [
                "3_global",
                "2_product_category",
                "1_product",
                "0_product_variant",
            ]:
                values.update(dict(sale_categ_id=None))
            elif applied_on == "2_0_product_sale_category":
                values.update(
                    dict(product_id=None, product_tmpl_id=None, categ_id=None)
                )
        return super().write(values)

    def _is_applicable_for(self, product, qty_in_product_uom):
        self.ensure_one()
        product.ensure_one()

        if (
            not (self.min_quantity and qty_in_product_uom < self.min_quantity)
            and self.applied_on == "2_0_product_sale_category"
        ):
            return product.sale_categ_id and (
                product.sale_categ_id == self.sale_categ_id
                or product.sale_categ_id.parent_path.startswith(
                    self.sale_categ_id.parent_path
                )
            )
        else:
            return super()._is_applicable_for(product, qty_in_product_uom)
