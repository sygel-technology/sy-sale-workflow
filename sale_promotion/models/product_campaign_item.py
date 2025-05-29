# Copyright 2025 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductCampaignItem(models.Model):
    _name = "product.campaign.item"
    _description = "Product Campaign Item"

    name = fields.Char(
        compute="_compute_name",
    )
    product_campaign_id = fields.Many2one(
        comodel_name="product.campaign", string="Campaign"
    )
    company_id = fields.Many2one(related="product_campaign_id.company_id")
    min_quantity = fields.Float(
        string="Min. Quantity",
        default=0,
        digits="Product Unit of Measure",
    )
    fixed_price = fields.Float(digits="Product Price")
    percent_price = fields.Float(
        string="Percentage Price",
    )
    date_start = fields.Datetime(
        string="Start Date",
    )
    date_end = fields.Datetime(
        string="Start End",
    )
    applied_on = fields.Selection(
        selection=[
            ("3_global", "All Products"),
            ("2_product_category", "Product Category"),
            ("1_product", "Product"),
            ("0_product_variant", "Product Variant"),
        ],
        string="Apply On",
        default="3_global",
    )
    compute_price = fields.Selection(
        selection=[
            ("fixed", "Fixed Price"),
            ("percentage", "Discount"),
        ],
        index=True,
        default="fixed",
        required=True,
    )
    categ_id = fields.Many2one(
        comodel_name="product.category",
        string="Product Category",
        ondelete="cascade",
    )
    product_tmpl_id = fields.Many2one(
        comodel_name="product.template",
        string="Product",
        ondelete="cascade",
        check_company=True,
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product Variant",
        ondelete="cascade",
        check_company=True,
    )

    @api.depends(
        "applied_on",
        "categ_id",
        "product_tmpl_id",
        "product_id",
        "compute_price",
        "fixed_price",
        "product_campaign_id",
        "percent_price",
    )
    def _compute_name(self):
        for item in self:
            if item.categ_id and item.applied_on == "2_product_category":
                item.name = _("Category: %s", item.categ_id.display_name)
            elif item.product_tmpl_id and item.applied_on == "1_product":
                item.name = _("Product: %s", item.product_tmpl_id.display_name)
            elif item.product_id and item.applied_on == "0_product_variant":
                item.name = _("Variant: %s", item.product_id.display_name)
            else:
                item.name = _("All Products")

    @api.constrains("product_id", "product_tmpl_id", "categ_id")
    def _check_product_consistency(self):
        for item in self:
            if item.applied_on == "2_product_category" and not item.categ_id:
                raise ValidationError(
                    _(
                        "Please specify the category for which this rule should "
                        "be applied"
                    )
                )
            elif item.applied_on == "1_product" and not item.product_tmpl_id:
                raise ValidationError(
                    _(
                        "Please specify the product for which this rule should be "
                        "applied"
                    )
                )
            elif item.applied_on == "0_product_variant" and not item.product_id:
                raise ValidationError(
                    _(
                        "Please specify the product variant for which this rule "
                        "should be applied"
                    )
                )

    def _is_applicable_for(self, product, qty_in_product_uom):
        self.ensure_one()
        product.ensure_one()
        res = True
        is_product_template = product._name == "product.template"
        if self.min_quantity and qty_in_product_uom < self.min_quantity:
            res = False
        elif self.applied_on == "2_product_category":
            if (
                product.categ_id != self.categ_id
                and not product.categ_id.parent_path.startswith(
                    self.categ_id.parent_path
                )
            ):
                res = False
        else:
            if is_product_template:
                if (
                    self.applied_on == "1_product"
                    and product.id != self.product_tmpl_id.id
                ):
                    res = False
                elif self.applied_on == "0_product_variant" and not (
                    product.product_variant_count == 1
                    and product.product_variant_id.id == self.product_id.id
                ):
                    res = False
            else:
                if (
                    self.applied_on == "1_product"
                    and product.product_tmpl_id.id != self.product_tmpl_id.id
                ):
                    res = False
                elif (
                    self.applied_on == "0_product_variant"
                    and product.id != self.product_id.id
                ):
                    res = False
        return res
