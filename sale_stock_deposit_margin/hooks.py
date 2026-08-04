# Copyright Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


def post_init_hook(env):
    """Set margin to 0 in old Delivery Stock Deposit Sale Order Lines"""
    routes = env["stock.route"].search(
        [
            ("deposit_operation", "=", True),
            ("deposit_operation_type", "=", "delivery_deposit"),
        ]
    )
    env["sale.order.line"].search([("route_id", "in", routes.ids)])._compute_margin()
