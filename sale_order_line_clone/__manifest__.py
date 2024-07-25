# Copyright 2024 Roger Sans <roger.sans@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Sale Order Line Clone",
    "version": "15.0.1.0.0",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Sales",
    "summary": "Clone sale order lines.",
    "website": "https://github.com/sygel-technology/sy-sale-workflow",
    "depends": [
        "product",
        "sale",
    ],
    "data": [
        "security/sale_order_line_clone_security.xml",
        "views/product_template_view.xml",
        "views/sale_order_view.xml",
    ],
}
