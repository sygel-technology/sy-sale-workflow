# Copyright 2022 Angel Garcia de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Automatic Monhly Invoicig",
    "summary": "Automatic Monhly Invoicig.",
    "version": "15.0.1.0.0",
    "category": "Accounting",
    "website": "https://github.com/sygel-technology/sy-sale-workflow",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "account",
        "sale",
    ],
    "data": [
        "data/cron.xml",
        "views/res_partner_views.xml",
        "views/sale_views.xml",
    ],
}
