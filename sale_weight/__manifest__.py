# Copyright 2020 Valentin Vinagre <valentin.vinagre@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Sale Weight',
    'version': '13.0.1.0.0',
    'category': 'Sale',
    'summary': 'Show weight in sale orders and sale order lines',
    'author': 'Sygel',
    'website': 'https://www.sygel.es',
    'license': 'AGPL-3',
    'depends': [
        'sale',
        'stock'
    ],
    'data': [
        'views/sale_order.xml'
    ],
    'installable': True,
}
