# Copyright 2023 Ángel García de la Chica <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "SO Group Stock User Read",
    "summary": "Sale Order Group Stock User Read",
    "version": "16.0.1.0.1",
    "category": "Sale",
    "website": "https://github.com/sygel-technology/sy-sale-workflow",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["base", "sales_team", "stock", "sale_stock"],
    "data": [
        "security/so_group_stock_user_read_security.xml",
        "views/sale_order_views.xml",
        "views/product_views.xml",
    ],
}
