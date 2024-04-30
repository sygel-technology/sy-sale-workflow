# Copyright 2023 Ángel García de la Chica <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Sale Report Hide Zero Discount",
    "summary": "Sale Report Hide Zero Discount",
    "version": "15.0.1.0.0",
    "category": "Sale",
    "website": "https://www.sygel.es",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        'sale_discount_display_amount'
    ],   
    "data": [
        "report/sale_report_templates.xml",
    ],
}
