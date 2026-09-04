# Copyright 2023 Valentin Vinagre <valentin.vinagre@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from . import models
from . import wizards


def _post_init_sale_stock_deposit(env):
    warehouses = env["stock.warehouse"].search([])
    env["stock.warehouse"]._create_deposits(warehouses)
