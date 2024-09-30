# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Queued SO Mail",
    "summary": "Module summary",
    "version": "12.0.1.0.0",
    "category": "Uncategorized",
    "website": "https://www.sygel.es",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
        "queue_job",
        "sale_order_type",
        "delivery"
    ],
    "data": [
        'views/res_partner_view.xml',
        'views/sale_order_type_view.xml',
        'views/delivery_view.xml',
        'views/sale_views.xml'
    ],
}
