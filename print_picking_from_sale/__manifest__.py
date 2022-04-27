# Copyright 2022 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Print Picking From Sale",
    "summary": "Print Sale Order as picking",
    "version": "14.0.1.0.0",
    "category": "Sales",
    "website": "https://www.sygel.es",
    "author": "Sygel",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "sale",
        "stock",
        "sale_stock",
        "web"
    ],
    "data": [
        "report/report_sale_complete_picking.xml",
        "data/report_sale_complete_picking_views.xml",
        "views/sale_order_views.xml"
    ],
}
