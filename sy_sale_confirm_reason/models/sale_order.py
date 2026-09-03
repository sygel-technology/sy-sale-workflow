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

    def _requires_confirm_reason(self):
        self.ensure_one()
        return False

    def _action_open_confirm_reason_wizard(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Confirmation Reason"),
            "res_model": "sale.confirm.reason.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_order_id": self.id,
            },
        }

    def action_confirm(self):
        if (
            len(self) == 1
            and self._requires_confirm_reason()
            and not self.confirm_reason_id
        ):
            result = self._action_open_confirm_reason_wizard()
        else:
            result = super().action_confirm()
        return result
