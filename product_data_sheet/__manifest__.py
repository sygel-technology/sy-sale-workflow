# Copyright 2020 Valentin Vinagre <valentin.vinagre@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Product Data Sheet',
    'version': '11.0.1.0.0',
    'category': 'Sale',
    'summary': 'Allow to attach data sheets in products and send them in sales.',
    'author': 'Sygel',
    'website': 'https://www.sygel.es',
    'license': 'AGPL-3',
    'depends': [
        'mail',
        'product',
        'sale',
    ],
    'data': [
        'views/product_template.xml',
        'views/mail_compose_message.xml'
    ],
    'installable': True,
}
