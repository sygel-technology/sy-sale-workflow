# Copyright 2026 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale Order Type Confirmation Reason",
    "summary": "Configure confirmation reasons by sale order type",
    "version": "18.0.1.0.0",
    "category": "Sales",
    "license": "AGPL-3",
    "website": "https://github.com/sygel-technology/sy-sale-workflow",
    "author": "Sygel",
    "depends": [
        "sy_sale_confirm_reason",
        "sale_order_type",
    ],
    "data": [
        "views/sale_order_type_views.xml",
    ],
    "installable": True,
}
