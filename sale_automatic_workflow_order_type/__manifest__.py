# Copyright 2023 Ángel García de la Chica <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Sale Automatic Workflow Order Type",
    "summary": "Sale Automatic Workflow Order Type",
    "version": "15.0.1.0.1",
    "category": "Sales Management",
    "website": "https://github.com/sygel-technology/sy-sale-workflow",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "sale_automatic_workflow",
        "sale_order_type",
    ],
    "data": [
        "views/sale_order_type_view.xml",
    ],
}
