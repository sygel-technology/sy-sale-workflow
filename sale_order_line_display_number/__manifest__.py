# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Sale Order Line Display Number",
    "summary": "Configure the number of sale order lines to be shown",
    "version": "15.0.1.0.0",
    "category": "Sale",
    "website": "https://github.com/sygel-technology/sy-sale-workflow",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "sale",
    ],
    "data": ["data/sale_order_line_display_number_data.xml"],
    "assets": {
        "web.assets_backend": [
            "sale_order_line_display_number/static/src/js/form_view.js",
        ]
    },
}
