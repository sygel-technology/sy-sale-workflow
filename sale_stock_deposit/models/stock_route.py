# Copyright 2023 Valentin Vinagre <valentin.vinagre@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockRoute(models.Model):
    _inherit = "stock.route"

    deposit_operation = fields.Boolean(
        "Deposit Operation?",
        default=False,
        help="Check this box to allow using this location to put deposit goods.",
    )
    deposit_operation_type = fields.Selection(
        selection=[
            ("deposit", "Deposit Sell"),
            ("delivery_deposit", "Delivery Stock Deposit"),
        ],
        default="deposit",
    )
    warehouse_id = fields.Many2one("stock.warehouse", "Warehouse")
