# Copyright 2026 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleConfirmReasonWizard(models.TransientModel):
    _name = "sale.confirm.reason.wizard"
    _description = "Sale Confirmation Reason Wizard"

    order_id = fields.Many2one(
        comodel_name="sale.order",
        required=True,
        readonly=True,
    )
    reason_id = fields.Many2one(
        comodel_name="sale.confirm.reason",
        string="Reason",
        required=True,
    )
    allow_manual_text = fields.Boolean(
        related="reason_id.allow_manual_text",
    )
    manual_text_required = fields.Boolean(
        related="reason_id.manual_text_required",
    )
    details = fields.Html(
        string="Additional Information",
    )

    @api.onchange("reason_id")
    def _onchange_reason_id(self):
        if not self.allow_manual_text:
            self.details = False

    def action_confirm(self):
        self.ensure_one()
        self.order_id.write(
            {
                "confirm_reason_id": self.reason_id.id,
                "confirm_reason_details": (
                    self.details if self.allow_manual_text else False
                ),
            }
        )
        return self.order_id.action_confirm()
