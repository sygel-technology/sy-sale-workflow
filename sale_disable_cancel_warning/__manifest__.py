# Copyright 2023 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale disable cancel warning",
    "summary": "Adds an option to disable the sale cancel warning wizard",
    "version": "16.0.1.0.0",
    "category": "Sale",
    "website": "https://github.com/sygel-technology/sy-sale-workflow",
    "author": "Alberto Martínez, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
        "sale",
    ],
    "data": [
        "views/res_config_settings.xml",
    ],
}
