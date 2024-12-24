# Copyright 2023 Valentin Vinagre <valentin.vinagre@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.osv import expression


class ProcurementGroup(models.Model):
    _inherit = "procurement.group"

    @api.model
    def _search_rule(self, route_ids, packaging_id, product_id, warehouse_id, domain):
        res = self.env["stock.rule"]
        partner_id = self.env.context.get("partner_id", False)
        if partner_id:
            partner = partner_id.commercial_partner_id
            Rule = self.env["stock.rule"]
            location = self.env["stock.location"].search(
                [
                    ("deposit_location", "=", True),
                    ("partner_id", "=", partner.id),
                    ("warehouse_id", "=", warehouse_id.id),
                ],
                limit=1,
            )
            if location:
                for route in route_ids.filtered(lambda x: x.deposit_operation):
                    if route.deposit_operation_type == "deposit":
                        new_domain = expression.AND(
                            [
                                [
                                    "|",
                                    ("warehouse_id", "=", warehouse_id.id),
                                    ("warehouse_id", "=", False),
                                    ("action", "!=", "push"),
                                    (
                                        "location_dest_id",
                                        "=",
                                        partner.property_stock_customer.id,
                                    ),
                                ]
                            ]
                        )
                    if route.deposit_operation_type == "delivery_deposit":
                        new_domain = expression.AND(
                            [
                                [
                                    "|",
                                    ("warehouse_id", "=", warehouse_id.id),
                                    ("warehouse_id", "=", False),
                                    ("action", "!=", "push"),
                                    (
                                        "location_dest_id",
                                        "!=",
                                        partner.property_stock_customer.id,
                                    ),
                                ]
                            ]
                        )
                    res = Rule.search(
                        expression.AND([[("route_id", "=", route.id)], new_domain]),
                        order="route_sequence, sequence",
                        limit=1,
                    )
        if not res:
            res = super()._search_rule(
                route_ids, packaging_id, product_id, warehouse_id, domain
            )
        return res

    @api.model
    def _get_rule(self, product_id, location_id, values):
        # The partner is passed by context to search for it in the rules domain
        context = dict(
            self.env.context,
            partner_id=self.env["res.partner"].browse(values.get("partner_id", False)),
        )
        return super(ProcurementGroup, self.with_context(**context))._get_rule(
            product_id, location_id, values
        )
