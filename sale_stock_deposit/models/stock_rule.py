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
        # This only works for the PULL rule, for the rest it would have to be modified.
        # venta deposito -> deposit
        #     origin(location_id)     dest
        #     WH/deposit(dinamic)     partners/customers

        # Delivery Deposit -> delivery_deposit
        #     origin                  dest(location_dest_id)
        #     WH/Stock                WH/deposit(dinamic)

        if (
            self.route_id.deposit_operation
            and self.route_id.deposit_operation_type
            in (
                "deposit",
                "delivery_deposit",
            )
        ):
            partner_id = self.env["res.partner"].browse(values.get("partner_id", False))
            domain = [
                ("partner_id", "=", partner_id.commercial_partner_id.id),
                ("deposit_location", "=", True),
            ]
            if values.get("warehouse_id", False):
                domain.append(("warehouse_id", "=", values.get("warehouse_id").id))
            location_id = self.env["stock.location"].search(domain, limit=1)
            if location_id:
                res[
                    "location_id"
                    if self.route_id.deposit_operation_type == "deposit"
                    else "location_dest_id"
                ] = location_id.id
        return res
