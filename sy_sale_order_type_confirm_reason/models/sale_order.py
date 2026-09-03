# Copyright 2026 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _show_confirm_reason_wizard(self):
        return not self.env.context.get("skip_sale_confirm_reason") and any(
            order.company_id.sale_confirm_reason
            and order.type_id.require_confirm_reason
            and not order.confirm_reason_id
            for order in self
        )
