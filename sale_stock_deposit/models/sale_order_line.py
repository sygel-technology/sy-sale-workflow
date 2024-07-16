# Copyright 2023 Valentin Vinagre <valentin.vinagre@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    route_id = fields.Many2one(
        domain="[('sale_selectable', '=', True), "
        "('warehouse_id', 'in', (False, warehouse_id))]"
    )

    def _prepare_invoice_line(self, **optional_values):
        """The 100% discount is set in case an invoice is issued."""
        res = super()._prepare_invoice_line(**optional_values)
        if (
            self.route_id.deposit_operation
            and self.route_id.deposit_operation_type == "delivery_deposit"
        ):
            res["discount"] = 100.0
        return res

    def write(self, values):
        """When configuring the routes and being a deposit delivery operation
        you would have to set the discount to 100%. You would not have to
        apply the sigaus either.
        """
        route_id = self.env["stock.route"].browse([values.get("route_id", False)])
        if (
            route_id
            and route_id.deposit_operation
            and route_id.deposit_operation_type == "delivery_deposit"
        ):
            values["discount"] = 100.0
        return super().write(values)

    @api.model_create_multi
    def create(self, values):
        """When configuring the routes and being a deposit delivery operation
        you would have to set the discount to 100%. You would not have to
        apply the sigaus either.
        """
        for val in values:
            route_id = self.env["stock.route"].browse([val.get("route_id", False)])
            if (
                route_id
                and route_id.deposit_operation
                and route_id.deposit_operation_type == "delivery_deposit"
            ):
                val["discount"] = 100.0
        return super().create(values)

    @api.onchange("route_id")
    def _onchange_route_id(self):
        for sel in self:
            res = 0.0
            if (
                sel.route_id
                and sel.route_id.deposit_operation
                and sel.route_id.deposit_operation_type == "delivery_deposit"
            ):
                res = 100.0
            sel.discount = res

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

    def _get_outgoing_incoming_moves(self):
        outgoing_moves, incoming_moves = super()._get_outgoing_incoming_moves()
        moves = self.move_ids.filtered(
            lambda r: r.state != "cancel"
            and not r.scrapped
            and self.product_id == r.product_id
        )
        if (
            self.route_id
            and self.route_id.deposit_operation
            and self.route_id.deposit_operation_type == "delivery_deposit"
        ):
            for move in moves:
                if not move.origin_returned_move_id or (
                    move.origin_returned_move_id and move.to_refund
                ):
                    outgoing_moves |= move
                elif move.to_refund:
                    incoming_moves |= move
        return outgoing_moves, incoming_moves
