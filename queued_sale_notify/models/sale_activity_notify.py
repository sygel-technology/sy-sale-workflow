# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class SaleActivityNotify(models.Model):
    _name = "sale.activity.notify"
    _description = "Sale Activity Notify"

    _inherit = ["activity.notify.mixin", "sale.notify.mixin"]
