# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _create_invoices(self, sale_orders):
        """Slice the batch according grouping criteria if using
        sale_order_invoicing_picking_filter's custom invoice creation
        """
        if not (self.advance_payment_method == "delivered" and self.stock_picking_ids):
            return super()._create_invoices()

        order_groups = {}
        for order in self.sale_order_ids:
            group_key = order._get_sale_invoicing_group_key()
            if group_key not in order_groups:
                order_groups[group_key] = order
            else:
                order_groups[group_key] += order
        moves = self.env["account.move"]
        for group in order_groups.values():
            moves += super()._create_invoices(group)
        return moves
