# Copyright 2023 Ángel García de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, models


class Warehouse(models.Model):
    _inherit = "stock.warehouse"

    def _get_vals_deposit_location(self, warehouse):
        return [
            {
                "name": _("{} / Deposit").format(warehouse.name),
                "usage": "view",
                "company_id": warehouse.company_id.id,
                "deposit_location": True,
                "location_id": warehouse.view_location_id.id,
            }
        ]

    def _get_vals_deposit_operation_type(
        self, warehouse, return_picking_id=False, deposit=False
    ):
        name = _("({}) Deposit Sale").format(warehouse.name)
        code = "incoming"
        sequence_code = f"{warehouse.code}/DEP_SALE/"
        print_label = False
        show_operations = False
        show_reserved = True
        default_location_src_id = self.env.ref("stock.stock_location_suppliers").id
        default_location_dest_id = warehouse.lot_stock_id.id
        if return_picking_id and deposit:
            name = _("({}) Delivery Stock Deposit").format(warehouse.name)
            code = "outgoing"
            sequence_code = f"{warehouse.code}/DEL_DEP/"
            print_label = True
            show_operations = True
            show_reserved = False
            default_location_src_id = deposit
            default_location_dest_id = self.env.ref("stock.stock_location_customers").id
        return [
            {
                "name": name,
                "code": code,
                "sequence_id": False,
                "sequence_code": sequence_code,
                "print_label": print_label,
                "reservation_method": "at_confirm",
                "company_id": warehouse.company_id.id,
                "return_picking_type_id": return_picking_id,
                "create_backorder": "ask",
                "show_operations": show_operations,
                "show_reserved": show_reserved,
                "use_create_lots": False,
                "use_existing_lots": True,
                "default_location_src_id": default_location_src_id,
                "default_location_dest_id": default_location_dest_id,
                "warehouse_id": warehouse.id,
            }
        ]

    def _get_vals_deposit_route(self, warehouse, deposit_operation_type):
        name = _("({}) / Deposit Sell").format(warehouse.name)
        if deposit_operation_type == "delivery_deposit":
            name = _("({}) / Delivery Stock Deposit").format(warehouse.name)
        return [
            {
                "name": name,
                "company_id": warehouse.company_id.id,
                "deposit_operation": True,
                "deposit_operation_type": deposit_operation_type,
                "warehouse_id": warehouse.id,
                "product_categ_selectable": False,
                "product_selectable": False,
                "warehouse_selectable": False,
                "sale_selectable": True,
            }
        ]

    def _get_vals_deposit_rule(self, warehouse, route, deposit, operation_type_id):
        name = _("{}/ Deposit -> Customer").format(warehouse.code)
        location_src_id = deposit
        location_dest_id = self.env.ref("stock.stock_location_customers")
        if route.deposit_operation_type == "delivery_deposit":
            name = _("{}/ Stock -> Deposit").format(warehouse.code)
            location_src_id = warehouse.lot_stock_id
            location_dest_id = deposit
        return [
            {
                "name": name,
                "action": "pull",
                "picking_type_id": operation_type_id.id,
                "location_src_id": location_src_id.id,
                "location_dest_id": location_dest_id.id,
                "procure_method": "make_to_stock",
                "warehouse_id": warehouse.id,
                "company_id": warehouse.company_id.id,
                "group_propagation_option": "propagate",
                "propagate_cancel": True,
                "route_id": route.id,
            }
        ]

    def _create_deposits(self, warehouses):
        for warehouse in warehouses:
            general_deposit_id = self.env["stock.location"].create(
                self._get_vals_deposit_location(warehouse)
            )
            type_incomming = self.env["stock.picking.type"].create(
                self._get_vals_deposit_operation_type(warehouse)
            )
            type_outgoing = self.env["stock.picking.type"].create(
                self._get_vals_deposit_operation_type(
                    warehouse, type_incomming.id, general_deposit_id.id
                )
            )
            type_incomming.return_picking_type_id = type_outgoing
            route_deposit_sell = self.env["stock.route"].create(
                self._get_vals_deposit_route(warehouse, "deposit")
            )
            route_delivery_deposit = self.env["stock.route"].create(
                self._get_vals_deposit_route(warehouse, "delivery_deposit")
            )
            self.env["stock.rule"].create(
                self._get_vals_deposit_rule(
                    warehouse, route_deposit_sell, general_deposit_id, type_incomming
                )
            )
            self.env["stock.rule"].create(
                self._get_vals_deposit_rule(
                    warehouse, route_delivery_deposit, general_deposit_id, type_outgoing
                )
            )

    @api.model_create_multi
    def create(self, vals_list):
        warehouses = super().create(vals_list)
        self._create_deposits(warehouses)
        return warehouses
