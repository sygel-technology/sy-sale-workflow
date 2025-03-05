# Copyright 2025 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Sale Promotion",
    "summary": "Sale Promotion",
    "version": "17.0.1.0.0",
    "category": "Sales",
    "website": "https://github.com/sygel-technology/sy-sale-workflow",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["sale"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_campaign_views.xml",
        "views/sale_campaign_views.xml",
        "views/sale_order_views.xml",
    ],
}
