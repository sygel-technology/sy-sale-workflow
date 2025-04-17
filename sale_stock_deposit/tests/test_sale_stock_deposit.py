# Copyright 2025 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError
from odoo.tests import Form, TransactionCase


class TestSaleStockDeposit(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        grp_multi_loc = cls.env.ref("stock.group_stock_multi_locations")
        cls.env.user.write({"groups_id": [(4, grp_multi_loc.id, 0)]})
        grp_lots = cls.env.ref("stock.group_production_lot")
        cls.env.user.write({"groups_id": [(4, grp_lots.id, 0)]})
        grp_multi_steps_route = cls.env.ref("stock.group_adv_location")
        cls.env.user.write({"groups_id": [(4, grp_multi_steps_route.id, 0)]})
        cls.company = cls.env.ref("base.main_company")
        cls.partner = cls.env["res.partner"].create({"name": "Test-Partner"})
        cls.main_warehouse = cls.env["stock.warehouse"].search(
            [("company_id", "=", cls.company.id)], limit=1
        )
        cls.main_deposit_location = cls.env["stock.location"].search(
            [
                ("company_id", "=", cls.company.id),
                ("warehouse_id", "=", cls.main_warehouse.id),
                ("deposit_location", "=", True),
                ("partner_id", "=", False),
            ],
            limit=1,
        )
        cls.sec_warehouse = cls.env["stock.warehouse"].create(
            {"company_id": cls.company.id, "code": "WH-2", "name": "Warehouse-2"}
        )
        cls.sec_deposit_location = cls.env["stock.location"].search(
            [
                ("company_id", "=", cls.company.id),
                ("warehouse_id", "=", cls.sec_warehouse.id),
                ("deposit_location", "=", True),
                ("partner_id", "=", False),
            ],
            limit=1,
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test-Product",
                "detailed_type": "product",
                "description_pickingout": "description_pickingout",
            }
        )

    def create_deposit(self, partner, location):
        wizard_values = partner.action_create_stock_deposit_wizard()
        wizard_form = Form(
            self.env[wizard_values["res_model"]].with_context(
                **wizard_values["context"]
            )
        )
        wizard_form.stock_deposit_id = location
        wizard = wizard_form.save()
        wizard.action_create()

    def create_deposit_sale(self, deposit_operation, qty=10):
        route = self.env["stock.route"].search(
            [
                ("warehouse_id", "=", self.main_warehouse.id),
                ("deposit_operation", "=", True),
                ("deposit_operation_type", "=", deposit_operation),
            ],
            limit=1,
        )
        order_form = Form(self.env["sale.order"])
        order_form.partner_id = self.partner
        order_form.warehouse_id = self.main_warehouse
        with order_form.order_line.new() as line_form:
            line_form.product_id = self.product
            line_form.product_uom_qty = qty
            line_form.route_id = route
        return order_form.save()

    def test_create_new_deposit(self):
        self.create_deposit(self.partner, self.main_deposit_location)
        self.assertEqual(len(self.partner.deposit_ids), 1)
        self.create_deposit(self.partner, self.sec_deposit_location)
        self.assertEqual(len(self.partner.deposit_ids), 2)

    def test_deposit_sale(self):

        # Create and validate deposit sale
        self.create_deposit(self.partner, self.main_deposit_location)
        order = self.create_deposit_sale("deposit")
        order.action_confirm()

        # Validate deposit sale picking
        picking = order.picking_ids[0]
        move = picking.move_ids[0]
        self.assertEqual(move.description_picking, self.product.description_pickingout)
        move.write({"quantity_done": 10})
        picking.button_validate()
        self.assertEqual(self.partner.deposit_count, 1)
        deposits = self.env["stock.quant"].search(
            [("location_id", "in", self.partner.deposit_ids.ids)]
        )
        self.assertEqual(len(deposits), 1)
        deposit = deposits[0]
        self.assertEqual(deposit.product_id, self.product)
        self.assertEqual(deposit.warehouse_id, self.main_warehouse)
        self.assertEqual(deposit.location_id, self.partner.deposit_ids[0])
        self.assertEqual(deposit.available_quantity, -10)
        self.assertEqual(deposit.quantity, -10)
        self.assertEqual(deposit.company_id, self.company)

        # Create and validate delivery stock deposit
        order = self.create_deposit_sale("delivery_deposit")
        order.action_confirm()
        picking = order.picking_ids[0]
        move = picking.move_ids[0]
        self.assertEqual(move.description_picking, self.product.description_pickingout)
        picking.move_ids[0].write({"quantity_done": 10})

        # Validate delivery stock deposit picking
        picking.button_validate()
        self.assertEqual(self.partner.deposit_count, 1)
        deposits = self.env["stock.quant"].search(
            [("location_id", "in", self.partner.deposit_ids.ids)]
        )
        self.assertEqual(len(deposits), 1)
        deposit = deposits[0]
        self.assertEqual(deposit.product_id, self.product)
        self.assertEqual(deposit.warehouse_id, self.main_warehouse)
        self.assertEqual(deposit.location_id, self.partner.deposit_ids[0])
        self.assertEqual(deposit.available_quantity, 0)
        self.assertEqual(deposit.quantity, 0)
        self.assertEqual(deposit.company_id, self.company)

    def test_partner_without_deposit_location(self):
        order = self.create_deposit_sale("deposit")
        self.env["stock.location"].search(
            [
                ("partner_id", "=", self.partner.id),
                ("deposit_location", "=", True),
                ("usage", "=", "internal"),
                ("warehouse_id", "=", self.main_warehouse.id),
            ],
            limit=1,
        ).unlink()
        with self.assertRaises(UserError):
            order.action_confirm()

    def test_deposit_not_enough_stock(self):
        self.create_deposit(self.partner, self.main_deposit_location)
        order = self.create_deposit_sale("deposit")
        order.action_confirm()
        picking = order.picking_ids[0]
        move = picking.move_ids[0]
        self.assertEqual(move.description_picking, self.product.description_pickingout)
        move.write({"quantity_done": 10})
        picking.button_validate()
        # Create and validate delivery stock deposit
        order = self.create_deposit_sale("delivery_deposit", 11)
        with self.assertRaises(UserError):
            order.action_confirm()

    def test_deposit_different_warehouse(self):
        self.create_deposit(self.partner, self.main_deposit_location)
        self.create_deposit(self.partner, self.sec_deposit_location)
        order = self.create_deposit_sale("deposit")
        route = self.env["stock.route"].search(
            [
                ("warehouse_id", "=", self.sec_warehouse.id),
                ("deposit_operation", "=", True),
                ("deposit_operation_type", "=", "deposit"),
            ],
            limit=1,
        )
        order.order_line[0].write({"route_id": route.id})
        with self.assertRaises(UserError):
            order.action_confirm()

    def test_deposit_already_exists(self):
        self.create_deposit(self.partner, self.main_deposit_location)
        with self.assertRaises(UserError):
            self.create_deposit(self.partner, self.main_deposit_location)
