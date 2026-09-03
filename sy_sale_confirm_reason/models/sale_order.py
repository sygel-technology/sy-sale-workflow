# Copyright 2026 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    confirm_reason_id = fields.Many2one(
        comodel_name="sale.confirm.reason",
        string="Confirmation",
        readonly=True,
        ondelete="restrict",
        tracking=True,
        copy=False,
    )
    confirm_reason_details = fields.Html(
        string="Details",
        readonly=True,
        copy=False,
    )

    def _action_open_confirm_reason_wizard(self):
        return {
            "type": "ir.actions.act_window",
            "name": _("Confirmation Reason"),
            "res_model": "sale.confirm.reason.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_order_ids": [fields.Command.set(self.ids)],
            },
        }

    def _show_confirm_reason_wizard(self):
        return not self.env.context.get("skip_sale_confirm_reason") and any(
            order.company_id.sale_confirm_reason and not order.confirm_reason_id
            for order in self
        )

    def action_confirm(self):
        if self._show_confirm_reason_wizard():
            result = self._action_open_confirm_reason_wizard()
        else:
            result = super().action_confirm()
        return result
