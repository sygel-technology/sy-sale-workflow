# Copyright 2023 Valentin Vinagre <valentin.vinagre@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from . import models
from . import wizards

from odoo import api, SUPERUSER_ID


def _post_init_sale_stock_deposit(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    warehouses = env["stock.warehouse"].search([])
    env["stock.warehouse"]._create_deposits(warehouses)
