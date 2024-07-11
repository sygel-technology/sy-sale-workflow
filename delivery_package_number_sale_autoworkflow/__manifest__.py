# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Delivery Package Number Sale Autoworkflow",
    "summary": "Make modules delivery_package_number and sale_automatic_workflow compatible",
    "version": "15.0.1.0.0",
    "category": "Picking",
    "website": "https://github.com/sygel-technology/sy-sale-workflow",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "sale_automatic_workflow",
        "delivery_package_number",
    ],
}
