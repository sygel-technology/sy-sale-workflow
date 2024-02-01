# Copyright 2023 Ángel García de la Chica <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Stock Picking Terms and Conditions",
    "summary": "Stock Picking Terms and Conditions",
    "version": "16.0.1.0.0",
    "category": "Stock",
    "website": "https://www.sygel.es",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        'base',
        'stock'
    ],   
    "data": [
        "views/stock_picking_views.xml",
        "views/res_config_settings_views.xml",
        "views/stock_picking_type_views.xml",
        "reports/report_deliveryslip.xml"
    ],
}
