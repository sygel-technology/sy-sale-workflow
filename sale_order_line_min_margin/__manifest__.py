# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Sale Order Line Min. Margin",
    "summary": "Set minimum margin in sale order lines",
    "version": "15.0.1.0.1",
    "category": "Product",
    "website": "https://github.com/sygel-technology/sy-sale-workflow",
    "author": "Sygel",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "sale_margin",
    ],
    "data": [
        "views/res_config_settings_views.xml",
    ],
}
