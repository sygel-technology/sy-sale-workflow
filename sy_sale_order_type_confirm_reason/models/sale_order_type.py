# Copyright 2026 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleOrderType(models.Model):
    _inherit = "sale.order.type"

    require_confirm_reason = fields.Boolean(
        string="Require Confirmation Reason",
        default=False,
        help="Require a confirmation reason when confirming sale orders of this type.",
    )
