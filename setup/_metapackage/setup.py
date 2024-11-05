import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-sygel-technology-sy-sale-workflow",
    description="Meta package for sygel-technology-sy-sale-workflow Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-print_picking_from_sale',
        'odoo14-addon-sale_automatic_workflow_order_type',
        'odoo14-addon-sale_order_high_priority',
        'odoo14-addon-so_line_open_form',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
