# Copyright 2023 Valentin Vinagre <valentin.vinagre@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.osv import expression


class ProcurementGroup(models.Model):
    _inherit = "procurement.group"

    @api.model
    def _get_deposit_rule(self, partner_id, warehouse_id, route_ids):
        # Auxiliar function to get the deposit stock rule
        #  given the procurement search parameters
        location_id = self.env["stock.location"].search(
            [
                ("deposit_location", "=", True),
                ("partner_id", "=", partner_id.id),
                ("warehouse_id", "=", warehouse_id.id),
            ],
            limit=1,
        )
        res = self.env["stock.rule"]
        if location_id and partner_id.deposit_ids:
            rule_domain = [
                "|",
                ("warehouse_id", "=", warehouse_id.id),
                ("warehouse_id", "=", False),
                ("action", "!=", "push"),
            ]
            for route in route_ids.filtered(lambda x: x.deposit_operation):
                if route.deposit_operation_type in ["deposit", "delivery_deposit"]:
                    new_domain = rule_domain + [
                        (
                            "location_dest_id",
                            "=" if route.deposit_operation_type == "deposit" else "!=",
                            partner_id.property_stock_customer.id,
                        )
                    ]
                    res = self.env["stock.rule"].search(
                        expression.AND([[("route_id", "=", route.id)], new_domain]),
                        order="route_sequence, sequence",
                        limit=1,
                    )
        return res

    @api.model
    def _get_rule(self, product_id, location_id, values):
        # If we are doing a deposit operation,
        # we override the method to return the deposit rule
        partner_id = self.env["res.partner"].browse(values.get("partner_id", False))
        warehouse_id = values.get("warehouse_id", location_id.warehouse_id)
        route_ids = values.get("route_ids", False)
        res = self._get_deposit_rule(partner_id, warehouse_id, route_ids)
        if not res:
            # The partner is passed by context to search for it in the rules domain
            context = dict(
                self.env.context,
                partner_id=partner_id,
            )
            res = super(ProcurementGroup, self.with_context(**context))._get_rule(
                product_id, location_id, values
            )
        return res

    @api.model
    def _search_rule(self, route_ids, packaging_id, product_id, warehouse_id, domain):
        # If we are doing a deposit operation,
        # we override the method to return the deposit rule.
        #
        # This function is called at the sale order confirmation
        # to get the rule that will set the move's values.
        #
        # Most of the rules are returned by _get_rule().abs
        # However, there can be uses cases where the rule is
        # obtained by this function
        res = self.env["stock.rule"]
        partner_id = self.env.context.get("partner_id", False)
        if partner_id:
            partner = partner_id.commercial_partner_id
            res = self._get_deposit_rule(partner, warehouse_id, route_ids)
        if not res:
            res = super()._search_rule(
                route_ids, packaging_id, product_id, warehouse_id, domain
            )
        return res
