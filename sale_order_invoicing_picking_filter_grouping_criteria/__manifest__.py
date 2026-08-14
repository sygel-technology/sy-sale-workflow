# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale Order Invoicing Picking Filter Grouping Criteria",
    "summary": "Glues the picking filter with sale_order_invoicing_grouping_criteria",
    "version": "18.0.1.0.0",
    "category": "Invoicing",
    "website": "https://github.com/sygel-technology/sy-sale-workflow",
    "author": "Sygel",
    "maintainers": ["tisho99"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "sale_order_invoicing_grouping_criteria",
        "sale_order_invoicing_picking_filter",
    ],
}
