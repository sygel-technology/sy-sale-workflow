# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class SaleMailNotify(models.Model):
    _name = "sale.mail.notify"
    _description = "Sale Mail Notify"

    _inherit = ["mail.notify.mixin", "sale.notify.mixin"]
