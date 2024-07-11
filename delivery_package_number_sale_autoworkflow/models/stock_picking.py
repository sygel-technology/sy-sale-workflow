# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def validate_picking(self):
        return super(
            StockPicking, self.with_context(bypass_set_number_of_packages=True)
        ).validate_picking()
