# Copyright 2023 Ángel García de la Chica <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "SO Sequence Confirmed Order Base",
    "summary": "Sale Order Sequence Confirmed Order Base",
    "version": "15.0.1.0.0",
    "category": "Sale",
    "website": "https://www.sygel.es",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    'conflicts': [
        'sale_quotation_number',
        'sale_order_type_quotation_number'
    ],
    "depends": [
        'base',
        'sale'
    ],   
    "data": [
        "views/res_config_settings_view.xml"
    ],
}
