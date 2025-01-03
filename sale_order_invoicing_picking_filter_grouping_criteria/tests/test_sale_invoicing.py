# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestSaleInvoiging(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(
            context=dict(
                cls.env.context,
                mail_create_nolog=True,
                mail_create_nosubscribe=True,
                mail_notrack=True,
                no_reset_password=True,
                tracking_disable=True,
            )
        )
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.partner = cls.env["res.partner"].create({"name": "Test partner"})
        cls.partner_delivery1 = cls.env["res.partner"].create(
            {
                "name": "Test delivery 1",
                "type": "delivery",
                "company_type": "person",
                "parent_id": cls.partner.id,
            }
        )
        cls.partner_delivery2 = cls.env["res.partner"].create(
            {
                "name": "Test delivery 2",
                "type": "delivery",
                "company_type": "person",
                "parent_id": cls.partner.id,
            }
        )
        cls.product = cls.env["product.product"].create(
            {"name": "Test product", "type": "product"}
        )
        cls.GroupingCriteria = cls.env["sale.invoicing.grouping.criteria"]
        cls.grouping_criteria = cls.GroupingCriteria.create(
            {
                "name": "Delivery Address",
                "field_ids": [
                    (4, cls.env.ref("sale.field_sale_order__partner_shipping_id").id)
                ],
            }
        )
        cls.order = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner.id,
                "partner_shipping_id": cls.partner_delivery1.id,
                "partner_invoice_id": cls.partner.id,
                "pricelist_id": cls.partner.property_product_pricelist.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": cls.product.name,
                            "product_id": cls.product.id,
                            "price_unit": 20,
                            "product_uom_qty": 1,
                            "product_uom": cls.product.uom_id.id,
                        },
                    )
                ],
            }
        )
        cls.order.action_confirm()
        cls.order2 = cls.order.copy()
        cls.order2.partner_shipping_id = cls.partner_delivery2
        cls.order2.action_confirm()

        for picking in (cls.order + cls.order2).picking_ids:
            picking.move_ids.write({"quantity_done": 1})
            picking._action_done()

    def create_invoicing_wizard(
        self, order_ids, picking_ids, invoice_service_products=False
    ):
        return self.env["sale.advance.payment.inv"].create(
            {
                "sale_order_ids": order_ids,
                "advance_payment_method": "delivered",
                "stock_picking_ids": picking_ids,
                "inv_service_products": invoice_service_products,
            }
        )

    def test_invoicing_no_grouping(self):
        invoice_ids = (self.order + self.order2)._create_invoices()
        self.assertEqual(len(invoice_ids), 1)
        self.assertEqual(self.order.invoice_ids, self.order2.invoice_ids)

    def test_invoicing_no_filtering(self):
        self.partner.sale_invoicing_grouping_criteria_id = self.grouping_criteria
        invoice_ids = (self.order + self.order2)._create_invoices()
        self.assertEqual(len(invoice_ids), 2)
        self.assertNotEqual(self.order.invoice_ids, self.order2.invoice_ids)

    def test_invoicing_picking_filtering(self):
        self.partner.sale_invoicing_grouping_criteria_id = self.grouping_criteria
        orders = self.order + self.order2
        wizard = self.create_invoicing_wizard(
            orders.mapped("id"),
            orders.mapped("picking_ids.id"),
        )
        invoice_ids = wizard._create_invoices(orders)
        self.assertEqual(len(invoice_ids), 2)
        self.assertNotEqual(self.order.invoice_ids, self.order2.invoice_ids)
