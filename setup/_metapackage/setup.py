import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-sygel-technology-sy-sale-workflow",
    description="Meta package for sygel-technology-sy-sale-workflow Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-product_search_category_attribute_sale>=16.0dev,<16.1dev',
        'odoo-addon-sale_category_pricelist>=16.0dev,<16.1dev',
        'odoo-addon-sale_disable_cancel_warning>=16.0dev,<16.1dev',
        'odoo-addon-sale_order_invoicing_picking_filter_grouping_criteria>=16.0dev,<16.1dev',
        'odoo-addon-sale_order_line_view_negative_margin>=16.0dev,<16.1dev',
        'odoo-addon-sale_stock_deposit>=16.0dev,<16.1dev',
        'odoo-addon-so_group_stock_user_read>=16.0dev,<16.1dev',
        'odoo-addon-so_line_open_form>=16.0dev,<16.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 16.0',
    ]
)
