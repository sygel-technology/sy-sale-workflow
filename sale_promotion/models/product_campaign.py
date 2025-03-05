# Copyright 2025 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductCampaign(models.Model):
    _name = "product.campaign"
    _description = "Promotion"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        comodel_name="res.company",
        default=lambda self: self.env.company,
    )
    product_campaign_item_ids = fields.One2many(
        comodel_name="product.campaign.item",
        inverse_name="product_campaign_id",
        string="Items",
    )

    def _get_applicable_rules_domain(self, products, date, **kwargs):
        self.ensure_one()
        if products._name == "product.template":
            templates_domain = ("product_tmpl_id", "in", products.ids)
            products_domain = ("product_id.product_tmpl_id", "in", products.ids)
        else:
            templates_domain = ("product_tmpl_id", "in", products.product_tmpl_id.ids)
            products_domain = ("product_id", "in", products.ids)

        return [
            ("product_campaign_id", "=", self.id),
            "|",
            ("categ_id", "=", False),
            ("categ_id", "parent_of", products.categ_id.ids),
            "|",
            ("product_tmpl_id", "=", False),
            templates_domain,
            "|",
            ("product_id", "=", False),
            products_domain,
            "|",
            ("date_start", "=", False),
            ("date_start", "<=", date),
            "|",
            ("date_end", "=", False),
            ("date_end", ">=", date),
        ]

    def _get_applicable_rules(self, products, date, **kwargs):
        self.ensure_one()
        if not self:
            return self.env["product.campaign.item"]
        return (
            self.env["product.campaign.item"]
            .with_context(active_test=False)
            .search(
                self._get_applicable_rules_domain(
                    products=products, date=date, **kwargs
                )
            )
            .with_context(**self.env.context)
        )
