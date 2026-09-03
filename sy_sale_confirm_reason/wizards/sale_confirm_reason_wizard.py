# Copyright 2026 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models, tools
from odoo.exceptions import ValidationError


class SaleConfirmReasonWizard(models.TransientModel):
    _name = "sale.confirm.reason.wizard"
    _description = "Sale Confirmation Reason Wizard"

    order_ids = fields.Many2many(
        comodel_name="sale.order",
        required=True,
        readonly=True,
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        compute="_compute_company_id",
    )
    reason_id = fields.Many2one(
        comodel_name="sale.confirm.reason",
        string="Reason",
        required=True,
        domain="[('company_id', '=', company_id)]",
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

    @api.depends("order_ids.company_id")
    def _compute_company_id(self):
        for wizard in self:
            wizard.company_id = wizard.order_ids.company_id[:1]

    @api.onchange("reason_id")
    def _onchange_reason_id(self):
        if not self.allow_manual_text:
            self.details = False

    def action_confirm(self):
        self.ensure_one()
        if any(
            order.company_id != self.reason_id.company_id for order in self.order_ids
        ):
            raise ValidationError(
                _("The confirmation reason must belong to the order company.")
            )
        if self.manual_text_required and tools.is_html_empty(self.details):
            raise ValidationError(
                _("Additional information is required for this reason.")
            )
        self.order_ids.write(
            {
                "confirm_reason_id": self.reason_id.id,
                "confirm_reason_details": (
                    self.details if self.allow_manual_text else False
                ),
            }
        )
        return self.order_ids.action_confirm()
