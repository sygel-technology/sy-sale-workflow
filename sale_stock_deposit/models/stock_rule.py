# Copyright 2023 Valentin Vinagre <valentin.vinagre@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class StockRule(models.Model):
    _inherit = "stock.rule"

    def _get_stock_move_values(
        self,
        product_id,
        product_qty,
        product_uom,
        location_id,
        name,
        origin,
        company_id,
        values,
    ):
        # Set the custom values that the deposit moves and its picking will have
        #
        # This function is called at the sale order confirmation, after searching
        # for the rule in thr procurement group, to set the move's values.
        #
        # This only works for the PULL rule, for the rest it would have to be modified.
        # venta deposito -> deposit
        #     origin(location_id)     dest
        #     WH/deposit(dinamic)     partners/customers
        #
        # Delivery Deposit -> delivery_deposit
        #     origin                  dest(location_dest_id)
        #     WH/Stock                WH/deposit(dinamic)
        res = super()._get_stock_move_values(
            product_id,
            product_qty,
            product_uom,
            location_id,
            name,
            origin,
            company_id,
            values,
        )

        if self.route_id.deposit_operation and self.route_id.deposit_operation_type in (
            "deposit",
            "delivery_deposit",
        ):
            partner_id = self.env["res.partner"].browse(values.get("partner_id", False))
            domain = [
                ("partner_id", "=", partner_id.commercial_partner_id.id),
                ("deposit_location", "=", True),
            ]
            if values.get("warehouse_id", False):
                domain.append(("warehouse_id", "=", values.get("warehouse_id").id))
            deposit_location_id = self.env["stock.location"].search(domain, limit=1)
            if deposit_location_id:
                deposit_operation_type = self.route_id.deposit_operation_type
                if deposit_operation_type == "deposit":
                    res["location_id"] = deposit_location_id.id
                    res["location_dest_id"] = self.env.ref(
                        "stock.stock_location_customers"
                    ).id
                elif deposit_operation_type == "delivery_deposit":
                    res["location_dest_id"] = deposit_location_id.id
        return res
