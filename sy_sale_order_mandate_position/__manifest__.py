# Copyright 2026 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale Order Mandate Position",
    "summary": "Moves the direct debit mandate next to the payment mode on sale orders",
    "version": "18.0.1.0.0",
    "category": "Sales",
    "author": "Sygel",
    "website": "https://github.com/sygel-technology/sy-sale-workflow",
    "license": "AGPL-3",
    "depends": [
        "account_banking_mandate_sale",
    ],
    "data": [
        "views/sale_order_views.xml",
    ],
    "installable": True,
}
