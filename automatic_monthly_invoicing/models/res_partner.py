# Copyright 2022 Angel Garcia de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    monthly_invoicing = fields.Boolean(
        help="A single invoice at the end of the month.",
        default=False,
        string="Automatic Monthly Invoicing",
    )
