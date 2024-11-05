import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo13-addons-sygel-technology-sy-sale-workflow",
    description="Meta package for sygel-technology-sy-sale-workflow Odoo addons",
    version=version,
    install_requires=[
        'odoo13-addon-pricelist_discount_decimal_accuracy',
        'odoo13-addon-sale_weight',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 13.0',
    ]
)
