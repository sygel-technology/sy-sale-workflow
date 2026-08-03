# Copyright 2023 Valentin Vinagre <valentin.vinagre@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        # Raise an error if the stock is not correct in a delivery_deposit operation
        for picking in self.filtered(lambda x: x.picking_type_code == "outgoing"):
            locations = picking.location_dest_id
            for move in picking.move_ids.filtered(
                lambda x: x.rule_id.route_id.deposit_operation
                and x.rule_id.route_id.deposit_operation_type == "delivery_deposit"
            ):
                qty_available = move.product_id.with_context(
                    location=locations.id
                ).qty_available
                if qty_available + move.quantity > 0:
                    raise UserError(
                        _(
                            "This client in your location does not have enough stock. "
                            f"The stock virtual in the location is {abs(qty_available)}"
                        )
                    )
        return super().button_validate()
