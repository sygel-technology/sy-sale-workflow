# Copyright 2025 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestSaleOrderWorkflowProcess(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.workflow_process = cls.env["sale.workflow.process"].create(
            {
                "name": "Sales Order Workflow Process",
            }
        )
        cls.order_type = cls.env["sale.order.type"].create(
            {
                "name": "Sales Order Type",
                "workflow_process_id": cls.workflow_process.id,
            }
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Partner",
            }
        )
        cls.sale_order = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner.id,
                "type_id": cls.order_type.id,
            }
        )
        cls.new_workflow_process = cls.env["sale.workflow.process"].create(
            {
                "name": "New Sales Order Workflow Process",
            }
        )
        cls.new_order_type = cls.env["sale.order.type"].create(
            {
                "name": "New Sales Order Type",
                "workflow_process_id": cls.new_workflow_process.id,
            }
        )

    def test_compute_workflow_process_id(self):
        self.assertEqual(
            self.sale_order.workflow_process_id, self.order_type.workflow_process_id
        )
        self.sale_order.type_id = self.new_order_type
        self.sale_order._compute_workflow_process_id()
        self.assertEqual(
            self.sale_order.workflow_process_id, self.new_order_type.workflow_process_id
        )
