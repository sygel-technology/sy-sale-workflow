# Copyright 2023 Ángel García de la Chica <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "SO Sequence Duplicate Order",
    "summary": "Sale Order Sequence Duplicate Order",
    "version": "15.0.1.0.0",
    "category": "Sale",
    "website": "https://www.sygel.es",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        'base',
        'sale'
    ],   
    "data": [
        "views/res_config_settings_view.xml"
    ],
}
