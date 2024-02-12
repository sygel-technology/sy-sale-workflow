# Copyright 2023 Valentin Vinagre <valentin.vinagre@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        """
        The lines with different routes from the default ones are searched and checked:
            * If they are deposit lines
            * If the customer has a warehouse location created.
            * If the warehouses configured between routes and sales are the same. 
        """
        for line in self.mapped('order_line').filtered(
           lambda x: x.route_id.id != x.warehouse_id.delivery_route_id.id):
            if line.route_id.deposit_operation:
                locations = self.env['stock.location'].search([
                    ('partner_id', '=', self.partner_id.id),
                    ('deposit_location', '=', True),
                    ('usage', '=', 'internal'),
                    ('warehouse_id', '=', self.warehouse_id.id)
                ], limit=1)
                if not locations:
                    raise UserError(_(
                        "The partner '{}' does not have "
                        "a deposit location configured!".format(
                            line.order_partner_id.display_name)
                        )
                    )
                if line.route_id.deposit_operation_type == 'delivery_deposit':
                    """ --->> A field can be created in the company to indicate 
                            whether to block or not, so that replenishments 
                            can be executed if necessary. 
                    """
                    qty_virtual = line.product_id.with_context(location=locations.id).virtual_available
                    total = qty_virtual + line.product_uom_qty
                    if total > 0:
                        raise UserError(_(
                            "The client '{}' in your location does not have "
                            "enough stock. The stock virtual in the location"
                            " is '{}' for the product '{}'".format(
                                line.order_partner_id.display_name, abs(qty_virtual), line.product_id.name
                            )
                        ))
            if line.route_id.warehouse_id and line.route_id.warehouse_id != line.warehouse_id:
                raise UserError(
                    _("Route's warehouse '{}' for product '{}' is not the same"
                      " as warehouse '{}' selected for the sale order.").format(
                        line.route_id.warehouse_id.display_name,
                        line.product_id.display_name,
                        line.warehouse_id.display_name,
                    )
                )
        return super(SaleOrder, self).action_confirm()