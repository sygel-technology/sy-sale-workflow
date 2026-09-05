# Copyright 2026 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, exceptions, fields, models


class SaleConfirmReason(models.Model):
    _name = "sale.confirm.reason"
    _description = "Sale Confirmation Reason"

    name = fields.Char(
        string="Reason",
        required=True,
        translate=True,
    )
    allow_manual_text = fields.Boolean(
        default=False,
    )
    manual_text_required = fields.Boolean(
        default=False,
    )

    _sql_constraints = [
        (
            "name_uniq",
            "unique(name)",
            "The confirmation reason must be unique.",
        ),
    ]

    @api.constrains("allow_manual_text", "manual_text_required")
    def _check_manual_text_required(self):
        for reason in self:
            if reason.manual_text_required and not reason.allow_manual_text:
                raise exceptions.ValidationError(
                    _("No additional information is required.")
                )

    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        default.setdefault("name", _("%s (copy)") % self.name)
        return super().copy(default)
