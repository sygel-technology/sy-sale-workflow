# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = ["sale.order", "confirmation.requirement.mixin"]
    _type_field = {
        "type": "type_id",
    }

    def action_confirm(self):
        ret_val = super().action_confirm()
        if ret_val:
            self.check_confirmation_requirements()
        return ret_val
