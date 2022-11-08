# Copyright 2022 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    priority = fields.Selection(
        selection_add=[
            ("2", "Very Urgent"),
        ]
    )


class SaleOrder(models.Model):
    _inherit = "sale.order"

    priority = fields.Selection(
        selection_add=[
            ("2", "Very Urgent"),
        ]
    )
