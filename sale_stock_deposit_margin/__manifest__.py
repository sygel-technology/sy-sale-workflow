# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale Stock Deposit Margin",
    "summary": "Module summary",
    "version": "16.0.1.0.0",
    "category": "Stock",
    "website": "https://github.com/sygel-technology/sy-sale-workflow",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "sale_stock_deposit",
        "sale_margin",
    ],
    "post_init_hook": "post_init_hook",
}
