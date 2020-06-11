# Copyright 2020 Valentin Vinagre <valentin.vinagre@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Sale Document Condition',
    'version': '11.0.1.0.0',
    'category': 'Sale',
    'summary': 'Allow define Multiple Templates for Conditions and use it on sale order.',
    'author': 'Sygel',
    'website': 'https://www.sygel.es',
    'license': 'AGPL-3',
    'depends': [
        'sale',
        'sales_team'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/sale_order_condition.xml',
        'views/sale_order.xml',
        'views/sale_order_report.xml'
    ],
    'installable': True,
}
