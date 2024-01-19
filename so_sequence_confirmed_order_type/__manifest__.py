# Copyright 2023 Ángel García de la Chica <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "SO Sequence Confirmed Order Type",
    "summary": "Sale Order Sequence Confirmed Order Type",
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
        'sale',
        'so_sequence_confirmed_order_base',
        'sale_order_type'
    ],   
    "data": [
        "views/sale_order_type_views.xml"
    ],
}
