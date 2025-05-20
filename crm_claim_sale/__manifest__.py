# Copyright 2022 Ángel García de la Chica <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "CRM Claim Sale",
    "summary": "Create Sales from a Claim",
    "version": "15.0.1.0.1",
    "category": "Sales/CRM",
    "website": "https://github.com/sygel-technology/sy-sale-workflow",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "crm_claim",
        "sale_order_type",
        "sale_crm",
    ],
    "data": [
        "views/crm_claim_views.xml",
        "views/sale_order_views.xml",
        "views/sale_order_type_view.xml",
    ],
}
