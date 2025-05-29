# Copyright 2025 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


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

    def action_apply_promotion(self):
        for line in self.filtered(
            lambda a: a.state != "cancel" and not a.order_id.locked and a.product_id
        ):
            lowest_rule = self.env["product.campaign.item"]
            lowest_price = (1 - line.discount / 100) * line.price_unit
            order = line.order_id
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
                    line.product_id, order.date_order
                )
            applicable_rules = self.env["product.campaign.item"]
            for rule in rules:
                if rule._is_applicable_for(line.product_id, line.product_uom_qty):
                    applicable_rules += rule
            if applicable_rules:
                for rule in applicable_rules:
                    if (
                        rule.compute_price == "fixed"
                        and rule.fixed_price < lowest_price
                    ):
                        lowest_price = rule.fixed_price
                        lowest_rule = rule
                    elif (
                        rule.compute_price == "percentage"
                        and (1 - rule.percent_price / 100) * line.price_unit
                        < lowest_price
                    ):
                        lowest_price = (1 - rule.percent_price / 100) * line.price_unit
                        lowest_rule = rule
            if lowest_rule:
                vals = {
                    "product_campaign_item_id": lowest_rule.id,
                }
                if lowest_rule.compute_price == "fixed":
                    line["price_unit"] = lowest_rule.fixed_price
                    line["discount"] = 0.0
                elif lowest_rule.compute_price == "percentage":
                    line["discount"] = lowest_rule.percent_price
                line.write(vals)
