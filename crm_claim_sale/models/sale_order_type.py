# Copyright 2022 Ángel García de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrderTypology(models.Model):
    _inherit = "sale.order.type"

    default_claim = fields.Boolean()

    @api.constrains("default_claim")
    def _checks_default_claim(self):
        res = self.search_count([("default_claim", "=", True)])
        if res > 1:
            raise ValidationError(
                _(
                    "There cannot be two types of Sales Orders with "
                    "'Default Claim' activated."
                )
            )
