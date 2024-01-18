# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Sale Order Line View Negative Margin",
    "summary": "Sale Order Line turns red if margin is 0 or negative",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Sygel",
    "category": "Sales",
    "depends": [
        "sale_margin",
    ],
    "data": [
        "views/sale_order_views.xml"
    ],
    "installable": True,
}
