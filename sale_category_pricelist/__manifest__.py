# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale Category Pricelist",
    "summary": "Adds a new type of categorization to pricelists",
    "version": "16.0.1.0.0",
    "category": "Sales/Sales",
    "website": "https://github.com/sygel-technology/sy-sale-workflow",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "account",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_pricelist_item_views.xml",
        "views/product_sale_category_views.xml",
        "views/product_views.xml",
    ],
}
