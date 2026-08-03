# Copyright 2023 Valentin Vinagre <valentin.vinagre@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import _, api, exceptions, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _prepare_invoice_line(self, **optional_values):
        """The 100% discount is set in case an invoice is issued."""
        res = super()._prepare_invoice_line(**optional_values)
        if (
            self.route_id.deposit_operation
            and self.route_id.deposit_operation_type == "delivery_deposit"
        ):
            res["discount"] = 100.0
        return res

    @api.depends("route_id")
    def _compute_discount(self):
        delivery_deposit_lines = self.filtered(
            lambda li: (
                li.route_id.deposit_operation
                and li.route_id.deposit_operation_type == "delivery_deposit"
            )
        )
        delivery_deposit_lines.discount = 100
        return super(SaleOrderLine, self - delivery_deposit_lines)._compute_discount()

    @api.depends("route_id")
    def _compute_invoice_status(self):
        res = super()._compute_invoice_status()
        for line in self.filtered(
            lambda x: x.route_id
            and x.route_id.deposit_operation
            and x.route_id.deposit_operation_type == "delivery_deposit"
        ):
            line.invoice_status = "no"
        return res

    @api.constrains("route_id", "warehouse_id")
    def _check_route_warehouse(self):
        invalid_lines = self.filtered(
            lambda li: li.route_id
            and li.route_id.warehouse_id not in (False, li.order_id.warehouse_id)
        )
        if invalid_lines:
            raise exceptions.UserError(
                _(
                    "The warehouse of the sale must be the same warehouse "
                    "of its line's routes"
                )
            )

    def _get_outgoing_incoming_moves(self, strict=True):
        # As our deposit moves have the origin and destination locations changed,
        # this function does place them correcly in the response.
        # We need to fix those moves and add them in the correct response place.
        outgoing_moves, incoming_moves = super()._get_outgoing_incoming_moves(strict)
        # First, remove deposit moves from the response, as they can be misplaced
        outgoing_moves = outgoing_moves.filtered(
            lambda m: not any(m.mapped("route_ids.deposit_operation"))
        )
        incoming_moves = incoming_moves.filtered(
            lambda m: not any(m.mapped("route_ids.deposit_operation"))
        )
        # Second, put the deposit moves in the correct place.
        # All of them are outgoing unless the case of returns
        moves = self.move_ids.filtered(
            lambda r: r.state != "cancel"
            and not r.scrapped
            and self.product_id == r.product_id
        )
        if self.route_id and self.route_id.deposit_operation:
            for move in moves:
                if not move.origin_returned_move_id:
                    outgoing_moves |= move
                else:
                    incoming_moves |= move
        return outgoing_moves, incoming_moves
