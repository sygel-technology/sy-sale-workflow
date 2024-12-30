This module dependencies provides 2 different ways of grouping the sale invoices:

- The Odoo's, developed in the sale module.
- The OCA's, developed in the sale_order_invoicing_grouping_criteria.

This module glues the OCA's function with the sale_order_invoicing_picking_filter. The Odoo function works perfectly with the sale_order_invoicing_picking_filter alone.

If a module that edits the Odoo's grouping function is installed it could be incompatible with the OCA grouping function.
