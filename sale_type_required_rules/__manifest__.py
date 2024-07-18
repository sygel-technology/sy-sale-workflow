# Copyright 2023 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Sale Type Required Rules",
    "version": "15.0.1.0.0",
    "summary": "Required domain conditions when validating a Sale Order.",
    "website": "https://github.com/sygel-technology/sy-sale-workflow",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Delivery",
    "depends": ["base", "sale", "sale_order_type"],
    "data": [
        "views/sale_order_type_view.xml",
        "views/sale_order_required_rule_views.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
    "auto_install": False,
}
