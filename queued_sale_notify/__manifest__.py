# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Queued Sale Notify",
    "summary": "Schedule email/logs/activities notificacions on sales",
    "version": "17.0.1.0.0",
    "category": "Sales",
    "website": "https://github.com/sygel-technology/sy-sale-workflow",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["sale_order_type", "delivery", "base_queued_notify"],
    "data": [
        "security/queued_sale_notify_security.xml",
        "security/ir.model.access.csv",
        "views/sale_order_type_view.xml",
    ],
}
