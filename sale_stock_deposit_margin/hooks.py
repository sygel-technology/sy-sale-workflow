# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import SUPERUSER_ID, api


def post_init_hook(cr, registry):
    """Set margin to 0 in old Delivery Stock Deposit Sale Order Lines"""
    env = api.Environment(cr, SUPERUSER_ID, {})
    routes = env["stock.route"].search(
        [
            ("deposit_operation", "=", True),
            ("deposit_operation_type", "=", "delivery_deposit"),
        ]
    )
    env["sale.order.line"].search([("route_id", "in", routes.ids)])._compute_margin()
