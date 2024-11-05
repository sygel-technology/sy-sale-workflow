import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-sygel-technology-sy-sale-workflow",
    description="Meta package for sygel-technology-sy-sale-workflow Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-sale_product_name_description',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 12.0',
    ]
)
