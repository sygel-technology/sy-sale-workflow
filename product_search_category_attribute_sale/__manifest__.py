# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product Search Category Attribute - Sale",
    "summary": "Search products in sales by category and attributes",
    "version": "16.0.1.0.0",
    "category": "Sales",
    "website": "https://github.com/sygel-technology/sy-sale-workflow",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["sale", "product_search_category_attribute"],
    "data": [
        "security/ir.model.access.csv",
        "wizards/product_search_category_attribute_views.xml",
        "views/sale_order_views.xml",
    ],
}
