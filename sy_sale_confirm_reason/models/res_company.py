# Copyright 2026 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    sale_confirm_reason = fields.Boolean(
        string="Sale Confirmation Reason",
        help="Ask for a reason when confirming a sales order.",
    )
