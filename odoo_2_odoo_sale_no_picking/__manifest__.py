# Copyright 2025 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Odoo 2 Odoo - No pickings in sales",
    "summary": """
        Avoid picking creation from sale orders created using Odoo 2
        Odoo Data Transfer""",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Sygel",
    "category": "Custom",
    "website": "https://github.com/sygel-technology/sy-sale-workflow",
    "depends": [
        "odoo_2_odoo_data_transfer",
        "sale_stock",
    ],
    "demo": [
        "demo/odoo.data.transfer.template.csv",
        "demo/odoo.data.transfer.template.line.csv",
    ],
    "installable": True,
}
