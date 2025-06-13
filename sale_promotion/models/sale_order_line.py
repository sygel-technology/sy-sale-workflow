# Copyright 2025 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.tools import float_compare


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_campaign_id = fields.Many2one(
        comodel_name="product.campaign",
        string="Product Campaign",
        ondelete="restrict",
        related="product_campaign_item_id.product_campaign_id",
        store=True,
    )
    product_campaign_item_id = fields.Many2one(
        comodel_name="product.campaign.item",
        string="Product Campaign Item",
        readonly=True,
        ondelete="restrict",
    )

    def _get_lowest_price_rule(self, applicable_rules, pricelist_price, lowest_price):
        # The method returns the current campaign rule in case it is
        # the rule with the lowest price
        lowest_rule = self.env["product.campaign.item"]
        for rule in applicable_rules:
            if rule.compute_price == "fixed" and (
                float_compare(
                    rule.fixed_price,
                    lowest_price,
                    precision_digits=self.order_id.currency_id.decimal_places,
                )
                < 0
                or (
                    not float_compare(
                        rule.fixed_price,
                        lowest_price,
                        precision_digits=self.order_id.currency_id.decimal_places,
                    )
                    and rule == self.product_campaign_item_id
                )
            ):
                lowest_price = rule.fixed_price
                lowest_rule = rule
            elif rule.compute_price == "percentage" and (
                float_compare(
                    (1 - rule.percent_price / 100) * pricelist_price,
                    lowest_price,
                    precision_digits=self.order_id.currency_id.decimal_places,
                )
                < 0
                or (
                    not float_compare(
                        (1 - rule.percent_price / 100) * pricelist_price,
                        lowest_price,
                        precision_digits=self.order_id.currency_id.decimal_places,
                    )
                    and rule == self.product_campaign_item_id
                )
            ):
                lowest_price = (1 - rule.percent_price / 100) * pricelist_price
                lowest_rule = rule
        return lowest_price, lowest_rule

    def _apply_promotion(self):
        self.ensure_one()
        lowest_rule = self.env["product.campaign.item"]

        # Current unit price
        lowest_price = (1 - self.discount / 100) * self.price_unit
        order = self.order_id

        # Unit price from pricelist
        pricelist_price = self._get_pricelist_price()
        if (
            float_compare(
                lowest_price,
                pricelist_price,
                precision_digits=self.order_id.currency_id.decimal_places,
            )
            > 0.0
        ):
            lowest_price = pricelist_price
        sale_campaigns = self.env["sale.campaign"].search(
            [
                ("pricelist_ids", "in", order.pricelist_id.id),
                "&",
                "|",
                ("start_date", "=", False),
                ("start_date", "<=", order.date_order),
                "|",
                ("end_date", "=", False),
                ("end_date", ">=", order.date_order),
            ]
        )
        product_campaigns = sale_campaigns.product_campaign_ids
        rules = self.env["product.campaign.item"]
        for product_campaign in product_campaigns:
            rules += product_campaign._get_applicable_rules(
                self.product_id, order.date_order
            )
        applicable_rules = self.env["product.campaign.item"]
        for rule in rules:
            if rule._is_applicable_for(self.product_id, self.product_uom_qty):
                applicable_rules += rule
        if applicable_rules:
            lowest_price, lowest_rule = self._get_lowest_price_rule(
                applicable_rules, pricelist_price, lowest_price
            )
        if lowest_rule:
            vals = {
                "product_campaign_item_id": lowest_rule.id,
            }
            discount = 0.0
            # Price without discount
            line = self.with_company(self.company_id)
            price = self._get_display_price()
            base_price = self.product_id._get_tax_included_unit_price_from_price(
                price,
                self.currency_id or self.order_id.currency_id,
                product_taxes=self.product_id.taxes_id.filtered(
                    lambda tax, line=line: tax.company_id == self.env.company
                ),
                fiscal_position=self.order_id.fiscal_position_id,
            )
            if base_price != 0.0:
                discount = (base_price - pricelist_price) / base_price * 100

            if self.order_id.pricelist_id.discount_policy == "with_discount":
                if lowest_rule.compute_price == "fixed":
                    vals.update(
                        {"price_unit": lowest_rule.fixed_price, "discount": 0.0}
                    )
                elif lowest_rule.compute_price == "percentage":
                    vals.update(
                        {
                            "price_unit": pricelist_price
                            - pricelist_price * (lowest_rule.percent_price / 100),
                            "discount": 0.0,
                        }
                    )
            elif (
                self.order_id.pricelist_id.discount_policy == "without_discount"
                and base_price != 0.0
            ):
                final_price = 0.0
                if lowest_rule.compute_price == "fixed":
                    final_price = lowest_rule.fixed_price
                elif lowest_rule.compute_price == "percentage":
                    final_price = pricelist_price - pricelist_price * (
                        lowest_rule.percent_price / 100
                    )
                extra_discount = ((base_price - final_price) * 100) / (
                    base_price * (discount or 1.0)
                )
                vals.update(
                    {
                        "price_unit": base_price,
                        "discount": extra_discount * (discount or 1.0),
                    }
                )
            self.write(vals)
        else:
            self.write({"product_campaign_item_id": False})
            # The pricelist price is the lowest price, so recompute the pricelist price
            if (
                float_compare(
                    pricelist_price,
                    lowest_price,
                    precision_digits=self.order_id.currency_id.decimal_places,
                )
                == 0.0
            ):
                self._compute_price_unit()
                self._compute_discount()

    def action_apply_promotion(self):
        for line in self.filtered(
            lambda a: a.state != "cancel" and not a.order_id.locked and a.product_id
        ):
            line._apply_promotion()
