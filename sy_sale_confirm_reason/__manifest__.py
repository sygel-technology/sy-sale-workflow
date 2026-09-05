# Copyright 2026 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale Confirm Reason",
    "summary": "Adds reasons for confirming sale orders",
    "version": "18.0.1.0.0",
    "category": "Sales",
    "website": "https://github.com/sygel-technology/sy-sale-workflow",
    "author": "Sygel",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "sale",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_confirm_reason_views.xml",
        "views/sale_order_views.xml",
        "wizards/sale_confirm_reason_wizard_views.xml",
    ],
}
