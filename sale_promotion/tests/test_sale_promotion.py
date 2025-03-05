# Copyright 2025 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo.tests import common, tagged


@tagged("post_install", "-at_install")
class TestPartnerDisableVatVerification(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_category = cls.env["product.category"].create(
            {
                "name": "Test-Category",
            }
        )
        cls.test_product = cls.env["product.product"].create(
            {
                "name": "Test-Product",
                "standard_price": 1,
                "categ_id": cls.test_category.id,
            }
        )
        cls.test_partner = cls.env["res.partner"].create(
            {
                "name": "Test-Partner",
            }
        )
        cls.test_pricelist = cls.env["product.pricelist"].create(
            {
                "name": "Test Pricelist",
                "item_ids": [
                    (
                        0,
                        0,
                        {
                            "applied_on": "0_product_variant",
                            "product_id": cls.test_product.id,
                            "compute_price": "fixed",
                            "fixed_price": 100,
                        },
                    ),
                ],
            }
        )
        cls.test_promotion_fixed_price = cls.env["product.campaign"].create(
            {
                "name": "Promotion-Fixed Price",
                "product_campaign_item_ids": [
                    (
                        0,
                        0,
                        {
                            "compute_price": "fixed",
                            "fixed_price": 100,
                            "applied_on": "3_global",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "compute_price": "fixed",
                            "fixed_price": 100,
                            "applied_on": "2_product_category",
                            "categ_id": cls.test_category.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "compute_price": "fixed",
                            "fixed_price": 100,
                            "applied_on": "1_product",
                            "product_tmpl_id": cls.test_product.product_tmpl_id.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "compute_price": "fixed",
                            "fixed_price": 100,
                            "applied_on": "0_product_variant",
                            "product_id": cls.test_product.id,
                        },
                    ),
                ],
            }
        )
        cls.test_promotion_percentage = cls.env["product.campaign"].create(
            {
                "name": "Promotion-Fixed Price",
                "product_campaign_item_ids": [
                    (
                        0,
                        0,
                        {
                            "compute_price": "percentage",
                            "percent_price": 0,
                            "applied_on": "3_global",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "compute_price": "percentage",
                            "percent_price": 0,
                            "applied_on": "2_product_category",
                            "categ_id": cls.test_category.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "compute_price": "percentage",
                            "percent_price": 0,
                            "applied_on": "1_product",
                            "product_tmpl_id": cls.test_product.product_tmpl_id.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "compute_price": "percentage",
                            "percent_price": 0,
                            "applied_on": "0_product_variant",
                            "product_id": cls.test_product.id,
                        },
                    ),
                ],
            }
        )
        cls.test_campaign = cls.env["sale.campaign"].create(
            {
                "name": "Test Campaign",
                "product_campaign_ids": [
                    cls.test_promotion_fixed_price.id,
                    cls.test_promotion_percentage.id,
                ],
                "pricelist_ids": [cls.test_pricelist.id],
            }
        )
        cls.sale_order = cls.env["sale.order"].create(
            {
                "partner_id": cls.test_partner.id,
                "pricelist_id": cls.test_pricelist.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.test_product.id,
                            "product_uom_qty": 1,
                        },
                    )
                ],
            }
        )

    def test_fixed_price_promotion(self):
        self.sale_order.action_apply_promotion()
        order_line = self.sale_order.order_line[0]
        self.assertFalse(order_line.discount)
        self.assertEqual(order_line.price_unit, 100)
        self.assertFalse(order_line.product_campaign_id)
        item = self.test_promotion_fixed_price.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "3_global"
        )
        item.write({"fixed_price": 90})
        self.sale_order.action_apply_promotion()
        self.assertFalse(order_line.discount)
        self.assertEqual(order_line.price_unit, 90)
        self.assertEqual(order_line.product_campaign_id, item.product_campaign_id)
        item = self.test_promotion_fixed_price.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "2_product_category"
        )
        item.write({"fixed_price": 80})
        self.sale_order.action_apply_promotion()
        self.assertFalse(order_line.discount)
        self.assertEqual(order_line.price_unit, 80)
        self.assertEqual(order_line.product_campaign_id, item.product_campaign_id)
        item = self.test_promotion_fixed_price.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "1_product"
        )
        item.write({"fixed_price": 70})
        self.sale_order.action_apply_promotion()
        self.assertFalse(order_line.discount)
        self.assertEqual(order_line.price_unit, 70)
        self.assertEqual(order_line.product_campaign_id, item.product_campaign_id)
        item = self.test_promotion_fixed_price.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "0_product_variant"
        )
        item.write({"fixed_price": 60})
        self.sale_order.action_apply_promotion()
        self.assertFalse(order_line.discount)
        self.assertEqual(order_line.price_unit, 60)
        self.assertEqual(order_line.product_campaign_id, item.product_campaign_id)

    def test_percenage_promotion(self):
        self.sale_order.action_apply_promotion()
        order_line = self.sale_order.order_line[0]
        self.assertFalse(order_line.discount)
        self.assertEqual(order_line.price_unit, 100)
        self.assertFalse(order_line.product_campaign_id)
        item = self.test_promotion_percentage.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "3_global"
        )
        item.write({"percent_price": 10})
        self.sale_order.action_apply_promotion()
        self.assertEqual(order_line.discount, 10)
        self.assertEqual(order_line.price_unit, 100)
        self.assertEqual(order_line.product_campaign_id, item.product_campaign_id)
        item = self.test_promotion_percentage.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "2_product_category"
        )
        item.write({"fixed_price": 20})
        self.sale_order.action_apply_promotion()
        self.assertEqual(order_line.discount, 10)
        self.assertEqual(order_line.price_unit, 100)
        self.assertEqual(order_line.product_campaign_id, item.product_campaign_id)
        item = self.test_promotion_percentage.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "1_product"
        )
        item.write({"fixed_price": 30})
        self.sale_order.action_apply_promotion()
        self.assertEqual(order_line.discount, 10)
        self.assertEqual(order_line.price_unit, 100)
        self.assertEqual(order_line.product_campaign_id, item.product_campaign_id)
        item = self.test_promotion_percentage.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "0_product_variant"
        )
        item.write({"fixed_price": 40})
        self.sale_order.action_apply_promotion()
        self.assertEqual(order_line.discount, 10)
        self.assertEqual(order_line.price_unit, 100)
        self.assertEqual(order_line.product_campaign_id, item.product_campaign_id)

    def test_min_qty_promotion(self):
        order_line = self.sale_order.order_line[0]
        item = self.test_promotion_fixed_price.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "3_global"
        )
        item.write({"fixed_price": 90, "min_quantity": 2})
        self.sale_order.action_apply_promotion()
        self.assertEqual(order_line.price_unit, 100)
        self.assertFalse(order_line.product_campaign_id)
        self.sale_order.order_line[0].write({"product_uom_qty": 2})
        self.sale_order.action_apply_promotion()
        self.assertEqual(order_line.price_unit, 90)
        self.assertEqual(order_line.product_campaign_id, item.product_campaign_id)

    def test_campaign_date_general_promotion(self):
        order_line = self.sale_order.order_line[0]
        item = self.test_promotion_fixed_price.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "3_global"
        )
        item.write(
            {
                "fixed_price": 90,
            }
        )
        self.test_campaign.write(
            {
                "start_date": self.sale_order.date_order + timedelta(days=1),
                "end_date": self.sale_order.date_order + timedelta(days=2),
            }
        )
        self.sale_order.action_apply_promotion()
        self.assertEqual(order_line.price_unit, 100)
        self.assertFalse(order_line.product_campaign_id)
        self.test_campaign.write(
            {
                "start_date": self.sale_order.date_order - timedelta(days=1),
                "end_date": self.sale_order.date_order + timedelta(days=2),
            }
        )
        self.sale_order.action_apply_promotion()
        self.assertEqual(order_line.price_unit, 90)
        self.assertEqual(order_line.product_campaign_id, item.product_campaign_id)

    def test_item_date_item_promotion(self):
        order_line = self.sale_order.order_line[0]
        item = self.test_promotion_fixed_price.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "3_global"
        )
        item.write(
            {
                "fixed_price": 90,
                "date_start": self.sale_order.date_order + timedelta(days=1),
                "date_end": self.sale_order.date_order + timedelta(days=2),
            }
        )
        self.sale_order.action_apply_promotion()
        self.assertEqual(order_line.price_unit, 100)
        self.assertFalse(order_line.product_campaign_id)
        item.write(
            {
                "date_start": self.sale_order.date_order - timedelta(days=1),
                "date_end": self.sale_order.date_order + timedelta(days=2),
            }
        )
        self.sale_order.action_apply_promotion()
        self.assertEqual(order_line.price_unit, 90)
        self.assertEqual(order_line.product_campaign_id, item.product_campaign_id)
