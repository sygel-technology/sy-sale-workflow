import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-sygel-technology-sy-sale-workflow",
    description="Meta package for sygel-technology-sy-sale-workflow Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-automatic_monthly_invoicing>=15.0dev,<15.1dev',
        'odoo-addon-crm_claim_sale>=15.0dev,<15.1dev',
        'odoo-addon-delivery_package_number_sale_autoworkflow>=15.0dev,<15.1dev',
        'odoo-addon-free_delivery_untaxed>=15.0dev,<15.1dev',
        'odoo-addon-sale_automatic_workflow_force_invoice>=15.0dev,<15.1dev',
        'odoo-addon-sale_automatic_workflow_order_type>=15.0dev,<15.1dev',
        'odoo-addon-sale_order_high_priority>=15.0dev,<15.1dev',
        'odoo-addon-sale_order_line_clone>=15.0dev,<15.1dev',
        'odoo-addon-sale_order_line_display_number>=15.0dev,<15.1dev',
        'odoo-addon-sale_order_line_min_margin>=15.0dev,<15.1dev',
        'odoo-addon-sale_type_confirmation_requirement_rules>=15.0dev,<15.1dev',
        'odoo-addon-sale_type_required_rules>=15.0dev,<15.1dev',
        'odoo-addon-so_line_description_picking>=15.0dev,<15.1dev',
        'odoo-addon-so_line_description_without_internal_ref>=15.0dev,<15.1dev',
        'odoo-addon-so_line_open_form>=15.0dev,<15.1dev',
        'odoo-addon-so_line_product_template_visibility>=15.0dev,<15.1dev',
        'odoo-addon-so_pricelist_lines_view>=15.0dev,<15.1dev',
        'odoo-addon-so_sequence_confirmed_order_base>=15.0dev,<15.1dev',
        'odoo-addon-so_sequence_confirmed_order_type>=15.0dev,<15.1dev',
        'odoo-addon-so_sequence_duplicate_confirmed_order_type>=15.0dev,<15.1dev',
        'odoo-addon-so_sequence_duplicate_order>=15.0dev,<15.1dev',
        'odoo-addon-state_sales_team_pricelist>=15.0dev,<15.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 15.0',
    ]
)
