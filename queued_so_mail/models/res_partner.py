# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class Partner(models.Model):
    _inherit = "res.partner"

    receive_confirmation_mails = fields.Boolean(
        string="Receive Sale Order Mails",
        default=True
    )
