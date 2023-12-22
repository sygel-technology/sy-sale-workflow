# Copyright 2023 Valentin Vinagre <valentin.vinagre@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Stock Deposit",
    "summary": "Stock deposit",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Sygel",
    "category": "Stock",
    "depends": [
        "sale",
        "sales_team",
        "stock",
        "sale_stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/stock_route.xml",
        "views/stock_location.xml",
        "views/res_partner_views.xml",
        "views/stock_quant_views.xml",
        "wizards/res_partner_stock_deposit_creation_wizard_views.xml"
    ],
    "installable": True,
    "post_init_hook": "_post_init_stock_deposit",
}
