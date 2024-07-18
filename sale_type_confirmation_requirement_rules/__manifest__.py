# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Sale Type Confirmation Requirement Rules",
    "version": "15.0.1.0.0",
    "summary": "Required domain conditions when validating a Sale Order.",
    "website": "https://github.com/sygel-technology/sy-sale-workflow",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Sales",
    "depends": [
        "sale_order_type",
        "base_confirmation_requirement_rules",
    ],
    "data": [
        "views/sale_order_type_view.xml",
        "views/sale_order_requirement_rule_views.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
    "auto_install": False,
}
