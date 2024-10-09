# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class SaleNoteNotify(models.Model):
    _name = "sale.log.note.notify"
    _description = "Sale Note Notify"

    _inherit = ["note.notify.mixin", "sale.notify.mixin"]
