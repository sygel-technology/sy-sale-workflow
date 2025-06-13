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
        cls.test_partner = cls.env["res.partner"].create(
            {
                "name": "Test-Partner",
            }
        )
        cls.test_product_1 = cls.env["product.product"].create(
            {
                "name": "Test-Product",
                "standard_price": 1,
                "categ_id": cls.test_category.id,
                "list_price": 100,
            }
        )
        cls.test_product_2 = cls.env["product.product"].create(
            {
                "name": "Test-Product",
                "standard_price": 1,
                "categ_id": cls.test_category.id,
                "list_price": 100,
            }
        )
        cls.test_pricelist_with_discount = cls.env["product.pricelist"].create(
            {
                "name": "Test Pricelist - With Discount",
                "discount_policy": "with_discount",
                "item_ids": [
                    (
                        0,
                        0,
                        {
                            "applied_on": "0_product_variant",
                            "product_id": cls.test_product_1.id,
                            "compute_price": "fixed",
                            "fixed_price": 100,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "applied_on": "0_product_variant",
                            "product_id": cls.test_product_2.id,
                            "compute_price": "percentage",
                            "percent_price": 10,
                        },
                    ),
                ],
            }
        )
        cls.test_pricelist_without_discount = cls.env["product.pricelist"].create(
            {
                "name": "Test Pricelist - Without Discount",
                "discount_policy": "without_discount",
                "item_ids": [
                    (
                        0,
                        0,
                        {
                            "applied_on": "0_product_variant",
                            "product_id": cls.test_product_1.id,
                            "compute_price": "fixed",
                            "fixed_price": 100,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "applied_on": "0_product_variant",
                            "product_id": cls.test_product_2.id,
                            "compute_price": "percentage",
                            "percent_price": 10,
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
                            "product_tmpl_id": cls.test_product_1.product_tmpl_id.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "compute_price": "fixed",
                            "fixed_price": 100,
                            "applied_on": "1_product",
                            "product_tmpl_id": cls.test_product_2.product_tmpl_id.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "compute_price": "fixed",
                            "fixed_price": 100,
                            "applied_on": "0_product_variant",
                            "product_id": cls.test_product_1.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "compute_price": "fixed",
                            "fixed_price": 100,
                            "applied_on": "0_product_variant",
                            "product_id": cls.test_product_2.id,
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
                            "product_tmpl_id": cls.test_product_1.product_tmpl_id.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "compute_price": "percentage",
                            "percent_price": 0,
                            "applied_on": "1_product",
                            "product_tmpl_id": cls.test_product_2.product_tmpl_id.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "compute_price": "percentage",
                            "percent_price": 0,
                            "applied_on": "0_product_variant",
                            "product_id": cls.test_product_1.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "compute_price": "percentage",
                            "percent_price": 0,
                            "applied_on": "0_product_variant",
                            "product_id": cls.test_product_2.id,
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
                "pricelist_ids": [
                    cls.test_pricelist_with_discount.id,
                    cls.test_pricelist_without_discount.id,
                ],
            }
        )

    def sale_promotion_sale_order(self, pricelist):
        return self.env["sale.order"].create(
            {
                "partner_id": self.test_partner.id,
                "pricelist_id": pricelist.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.test_product_1.id,
                            "product_uom_qty": 1,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "product_id": self.test_product_2.id,
                            "product_uom_qty": 1,
                        },
                    ),
                ],
            }
        )

    def test_pricelist_with_discount_fixed_price(self):
        sale_order = self.sale_promotion_sale_order(self.test_pricelist_with_discount)
        product_1_line = sale_order.order_line.filtered(
            lambda line: line.product_id == self.test_product_1
        )
        product_2_line = sale_order.order_line.filtered(
            lambda line: line.product_id == self.test_product_2
        )
        self.assertEqual(product_1_line.price_unit, 100)
        self.assertEqual(product_2_line.price_unit, 90)

        # Global item
        item = self.test_promotion_fixed_price.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "3_global"
        )
        item.write({"fixed_price": 80})
        sale_order.action_apply_promotion()
        self.assertFalse(product_1_line.discount)
        self.assertEqual(product_1_line.price_unit, 80)
        self.assertFalse(product_2_line.discount)
        self.assertEqual(product_2_line.price_unit, 80)
        self.assertEqual(product_1_line.product_campaign_item_id, item)
        self.assertEqual(product_2_line.product_campaign_item_id, item)

        # Product Category item
        item = self.test_promotion_fixed_price.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "2_product_category"
        )
        item.write({"fixed_price": 70})
        sale_order.action_apply_promotion()
        self.assertFalse(product_1_line.discount)
        self.assertEqual(product_1_line.price_unit, 70)
        self.assertFalse(product_2_line.discount)
        self.assertEqual(product_2_line.price_unit, 70)
        self.assertEqual(product_1_line.product_campaign_item_id, item)
        self.assertEqual(product_2_line.product_campaign_item_id, item)

        # Product Category item
        item = self.test_promotion_fixed_price.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "2_product_category"
        )
        item.write({"fixed_price": 60})
        sale_order.action_apply_promotion()
        self.assertFalse(product_1_line.discount)
        self.assertEqual(product_1_line.price_unit, 60)
        self.assertFalse(product_2_line.discount)
        self.assertEqual(product_2_line.price_unit, 60)
        self.assertEqual(product_1_line.product_campaign_item_id, item)
        self.assertEqual(product_2_line.product_campaign_item_id, item)

        # Product Template Item
        item_1 = self.test_promotion_fixed_price.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "1_product"
            and item.product_tmpl_id == self.test_product_1.product_tmpl_id
        )
        item_1.write({"fixed_price": 50})
        item_2 = self.test_promotion_fixed_price.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "1_product"
            and item.product_tmpl_id == self.test_product_2.product_tmpl_id
        )
        item_2.write({"fixed_price": 50})
        sale_order.action_apply_promotion()
        self.assertFalse(product_1_line.discount)
        self.assertEqual(product_1_line.price_unit, 50)
        self.assertFalse(product_2_line.discount)
        self.assertEqual(product_2_line.price_unit, 50)
        self.assertEqual(product_1_line.product_campaign_item_id, item_1)
        self.assertEqual(product_2_line.product_campaign_item_id, item_2)

        # Product Variant Item
        item_1 = self.test_promotion_fixed_price.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "0_product_variant"
            and item.product_id == self.test_product_1
        )
        item_1.write({"fixed_price": 40})
        item_2 = self.test_promotion_fixed_price.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "0_product_variant"
            and item.product_id == self.test_product_2
        )
        item_2.write({"fixed_price": 40})
        sale_order.action_apply_promotion()
        self.assertFalse(product_1_line.discount)
        self.assertEqual(product_1_line.price_unit, 40)
        self.assertFalse(product_2_line.discount)
        self.assertEqual(product_2_line.price_unit, 40)
        self.assertEqual(product_1_line.product_campaign_item_id, item_1)
        self.assertEqual(product_2_line.product_campaign_item_id, item_2)

        # No promotion applied - Recompute pricelist price
        self.test_pricelist_with_discount.item_ids.filtered(
            lambda item: item.product_id == self.test_product_1
        ).write(
            {
                "fixed_price": 20,
            }
        )
        self.test_pricelist_with_discount.item_ids.filtered(
            lambda item: item.product_id == self.test_product_2
        ).write(
            {
                "percent_price": 80,
            }
        )
        sale_order.action_apply_promotion()
        self.assertFalse(product_1_line.discount)
        self.assertEqual(product_1_line.price_unit, 20)
        self.assertFalse(product_2_line.discount)
        self.assertEqual(product_2_line.price_unit, 20)
        self.assertFalse(product_1_line.product_campaign_item_id)
        self.assertFalse(product_2_line.product_campaign_item_id)

        # Manually changed price/discount. Keep price/discount
        product_1_line.write({"price_unit": 10})
        product_2_line.write({"price_unit": 100, "discount": 90})
        sale_order.action_apply_promotion()
        self.assertFalse(product_1_line.discount)
        self.assertEqual(product_1_line.price_unit, 10)
        self.assertEqual(product_2_line.discount, 90)
        self.assertEqual(product_2_line.price_unit, 100)
        self.assertFalse(product_1_line.product_campaign_item_id)
        self.assertFalse(product_2_line.product_campaign_item_id)

    def test_pricelist_with_discount_percentage(self):
        sale_order = self.sale_promotion_sale_order(self.test_pricelist_with_discount)
        product_1_line = sale_order.order_line.filtered(
            lambda line: line.product_id == self.test_product_1
        )
        product_2_line = sale_order.order_line.filtered(
            lambda line: line.product_id == self.test_product_2
        )
        self.assertEqual(product_1_line.price_unit, 100)
        self.assertEqual(product_2_line.price_unit, 90)

        # Global item
        item = self.test_promotion_percentage.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "3_global"
        )
        item.write({"percent_price": 20})
        sale_order.action_apply_promotion()
        self.assertFalse(product_1_line.discount)
        self.assertEqual(product_1_line.price_unit, 80)
        self.assertFalse(product_2_line.discount)
        self.assertEqual(product_2_line.price_unit, 72)
        self.assertEqual(product_1_line.product_campaign_item_id, item)
        self.assertEqual(product_2_line.product_campaign_item_id, item)

        # Product Category item
        item = self.test_promotion_percentage.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "2_product_category"
        )
        item.write({"percent_price": 30})
        sale_order.action_apply_promotion()
        self.assertFalse(product_1_line.discount)
        self.assertEqual(product_1_line.price_unit, 70)
        self.assertFalse(product_2_line.discount)
        self.assertEqual(product_2_line.price_unit, 63)
        self.assertEqual(product_1_line.product_campaign_item_id, item)
        self.assertEqual(product_2_line.product_campaign_item_id, item)

        # Product Category item
        item = self.test_promotion_percentage.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "2_product_category"
        )
        item.write({"percent_price": 40})
        sale_order.action_apply_promotion()
        self.assertFalse(product_1_line.discount)
        self.assertEqual(product_1_line.price_unit, 60)
        self.assertFalse(product_2_line.discount)
        self.assertEqual(product_2_line.price_unit, 54)
        self.assertEqual(product_1_line.product_campaign_item_id, item)
        self.assertEqual(product_2_line.product_campaign_item_id, item)

        # Product Template Item
        item_1 = self.test_promotion_percentage.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "1_product"
            and item.product_tmpl_id == self.test_product_1.product_tmpl_id
        )
        item_1.write({"percent_price": 50})
        item_2 = self.test_promotion_percentage.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "1_product"
            and item.product_tmpl_id == self.test_product_2.product_tmpl_id
        )
        item_2.write({"percent_price": 50})
        sale_order.action_apply_promotion()
        self.assertFalse(product_1_line.discount)
        self.assertEqual(product_1_line.price_unit, 50)
        self.assertFalse(product_2_line.discount)
        self.assertEqual(product_2_line.price_unit, 45)
        self.assertEqual(product_1_line.product_campaign_item_id, item_1)
        self.assertEqual(product_2_line.product_campaign_item_id, item_2)

        # Product Variant Item
        item_1 = self.test_promotion_percentage.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "0_product_variant"
            and item.product_id == self.test_product_1
        )
        item_1.write({"percent_price": 60})
        item_2 = self.test_promotion_percentage.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "0_product_variant"
            and item.product_id == self.test_product_2
        )
        item_2.write({"percent_price": 60})
        sale_order.action_apply_promotion()
        self.assertFalse(product_1_line.discount)
        self.assertEqual(product_1_line.price_unit, 40)
        self.assertFalse(product_2_line.discount)
        self.assertEqual(product_2_line.price_unit, 36)
        self.assertEqual(product_1_line.product_campaign_item_id, item_1)
        self.assertEqual(product_2_line.product_campaign_item_id, item_2)

        # No promotion applied - Recompute pricelist price
        item = self.test_promotion_percentage.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "3_global"
        )
        item.write({"percent_price": -50})

        item = self.test_promotion_percentage.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "2_product_category"
        )
        item.write({"percent_price": -50})
        item_1 = self.test_promotion_percentage.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "1_product"
            and item.product_tmpl_id == self.test_product_1.product_tmpl_id
        )
        item_1.write({"percent_price": -50})
        item_2 = self.test_promotion_percentage.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "1_product"
            and item.product_tmpl_id == self.test_product_2.product_tmpl_id
        )
        item_2.write({"percent_price": -50})
        item_1 = self.test_promotion_percentage.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "0_product_variant"
            and item.product_id == self.test_product_1
        )
        item_1.write({"percent_price": -50})
        item_2 = self.test_promotion_percentage.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "0_product_variant"
            and item.product_id == self.test_product_2
        )
        item_2.write({"percent_price": -50})
        self.test_pricelist_with_discount.item_ids.filtered(
            lambda item: item.product_id == self.test_product_1
        ).write(
            {
                "fixed_price": 20,
            }
        )
        self.test_pricelist_with_discount.item_ids.filtered(
            lambda item: item.product_id == self.test_product_2
        ).write(
            {
                "percent_price": 80,
            }
        )
        sale_order.action_apply_promotion()
        self.assertFalse(product_1_line.discount)
        self.assertEqual(product_1_line.price_unit, 20)
        self.assertFalse(product_2_line.discount)
        self.assertEqual(product_2_line.price_unit, 20)
        self.assertFalse(product_1_line.product_campaign_item_id)
        self.assertFalse(product_2_line.product_campaign_item_id)

        # Manually changed price/discount. Keep price/discount
        product_1_line.write({"price_unit": 10})
        product_2_line.write({"price_unit": 100, "discount": 90})
        sale_order.action_apply_promotion()
        self.assertFalse(product_1_line.discount)
        self.assertEqual(product_1_line.price_unit, 10)
        self.assertEqual(product_2_line.discount, 90)
        self.assertEqual(product_2_line.price_unit, 100)
        self.assertFalse(product_1_line.product_campaign_item_id)
        self.assertFalse(product_2_line.product_campaign_item_id)

    def test_pricelist_without_discount_fixed_price(self):
        sale_order = self.sale_promotion_sale_order(
            self.test_pricelist_without_discount
        )
        product_1_line = sale_order.order_line.filtered(
            lambda line: line.product_id == self.test_product_1
        )
        product_2_line = sale_order.order_line.filtered(
            lambda line: line.product_id == self.test_product_2
        )
        self.assertEqual(product_1_line.price_unit, 100)
        self.assertEqual(product_1_line.discount, 0)
        self.assertEqual(product_2_line.price_unit, 100)
        self.assertEqual(product_2_line.discount, 10)

        # Global item
        item = self.test_promotion_fixed_price.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "3_global"
        )
        item.write({"fixed_price": 80})
        sale_order.action_apply_promotion()
        self.assertEqual(product_1_line.price_unit, 100)
        self.assertEqual(product_1_line.discount, 20)
        self.assertEqual(product_2_line.price_unit, 100)
        self.assertEqual(product_2_line.discount, 20)
        self.assertEqual(product_1_line.product_campaign_item_id, item)
        self.assertEqual(product_2_line.product_campaign_item_id, item)

        # Product Category item
        item = self.test_promotion_fixed_price.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "2_product_category"
        )
        item.write({"fixed_price": 70})
        sale_order.action_apply_promotion()
        self.assertEqual(product_1_line.price_unit, 100)
        self.assertEqual(product_1_line.discount, 30)
        self.assertEqual(product_2_line.price_unit, 100)
        self.assertEqual(product_2_line.discount, 30)
        self.assertEqual(product_1_line.product_campaign_item_id, item)
        self.assertEqual(product_2_line.product_campaign_item_id, item)

        # Product Category item
        item = self.test_promotion_fixed_price.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "2_product_category"
        )
        item.write({"fixed_price": 60})
        sale_order.action_apply_promotion()
        self.assertEqual(product_1_line.price_unit, 100)
        self.assertEqual(product_1_line.discount, 40)
        self.assertEqual(product_2_line.price_unit, 100)
        self.assertEqual(product_2_line.discount, 40)
        self.assertEqual(product_1_line.product_campaign_item_id, item)
        self.assertEqual(product_2_line.product_campaign_item_id, item)

        # Product Template Item
        item_1 = self.test_promotion_fixed_price.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "1_product"
            and item.product_tmpl_id == self.test_product_1.product_tmpl_id
        )
        item_1.write({"fixed_price": 50})
        item_2 = self.test_promotion_fixed_price.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "1_product"
            and item.product_tmpl_id == self.test_product_2.product_tmpl_id
        )
        item_2.write({"fixed_price": 50})
        sale_order.action_apply_promotion()
        self.assertEqual(product_1_line.price_unit, 100)
        self.assertEqual(product_1_line.discount, 50)
        self.assertEqual(product_2_line.price_unit, 100)
        self.assertEqual(product_2_line.discount, 50)
        self.assertEqual(product_1_line.product_campaign_item_id, item_1)
        self.assertEqual(product_2_line.product_campaign_item_id, item_2)

        # Product Variant Item
        item_1 = self.test_promotion_fixed_price.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "0_product_variant"
            and item.product_id == self.test_product_1
        )
        item_1.write({"fixed_price": 40})
        item_2 = self.test_promotion_fixed_price.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "0_product_variant"
            and item.product_id == self.test_product_2
        )
        item_2.write({"fixed_price": 40})
        sale_order.action_apply_promotion()
        self.assertEqual(product_1_line.price_unit, 100)
        self.assertEqual(product_1_line.discount, 60)
        self.assertEqual(product_2_line.price_unit, 100)
        self.assertEqual(product_2_line.discount, 60)
        self.assertEqual(product_1_line.product_campaign_item_id, item_1)
        self.assertEqual(product_2_line.product_campaign_item_id, item_2)

        # No promotion applied - Recompute pricelist price
        self.test_pricelist_without_discount.item_ids.filtered(
            lambda item: item.product_id == self.test_product_1
        ).write(
            {
                "fixed_price": 20,
            }
        )
        self.test_pricelist_without_discount.item_ids.filtered(
            lambda item: item.product_id == self.test_product_2
        ).write(
            {
                "percent_price": 80,
            }
        )
        sale_order.action_apply_promotion()
        self.assertEqual(product_1_line.price_unit, 100)
        self.assertEqual(product_1_line.discount, 80)
        self.assertEqual(product_2_line.price_unit, 100)
        self.assertEqual(product_2_line.discount, 80)
        self.assertFalse(product_1_line.product_campaign_item_id)
        self.assertFalse(product_2_line.product_campaign_item_id)

        # Manually changed price/discount. Keep price/discount
        product_1_line.write({"price_unit": 10, "discount": 0})
        product_2_line.write({"price_unit": 100, "discount": 90})
        sale_order.action_apply_promotion()
        self.assertEqual(product_1_line.price_unit, 10)
        self.assertEqual(product_1_line.discount, 0)
        self.assertEqual(product_2_line.price_unit, 100)
        self.assertEqual(product_2_line.discount, 90)
        self.assertFalse(product_1_line.product_campaign_item_id)
        self.assertFalse(product_2_line.product_campaign_item_id)

    def test_pricelist_without_discount_percentage(self):
        sale_order = self.sale_promotion_sale_order(
            self.test_pricelist_without_discount
        )
        product_1_line = sale_order.order_line.filtered(
            lambda line: line.product_id == self.test_product_1
        )
        product_2_line = sale_order.order_line.filtered(
            lambda line: line.product_id == self.test_product_2
        )
        self.assertEqual(product_1_line.price_unit, 100)
        self.assertEqual(product_1_line.discount, 0)
        self.assertEqual(product_2_line.price_unit, 100)
        self.assertEqual(product_2_line.discount, 10)

        # Global item
        item = self.test_promotion_percentage.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "3_global"
        )
        item.write({"percent_price": 20})
        sale_order.action_apply_promotion()
        self.assertEqual(product_1_line.price_unit, 100)
        self.assertEqual(product_1_line.discount, 20)
        self.assertEqual(product_2_line.price_unit, 100)
        self.assertEqual(product_2_line.discount, 28)
        self.assertEqual(product_1_line.product_campaign_item_id, item)
        self.assertEqual(product_2_line.product_campaign_item_id, item)

        # Product Category item
        item = self.test_promotion_percentage.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "2_product_category"
        )
        item.write({"percent_price": 30})
        sale_order.action_apply_promotion()
        self.assertEqual(product_1_line.price_unit, 100)
        self.assertEqual(product_1_line.discount, 30)
        self.assertEqual(product_2_line.price_unit, 100)
        self.assertEqual(product_2_line.discount, 37)
        self.assertEqual(product_1_line.product_campaign_item_id, item)
        self.assertEqual(product_2_line.product_campaign_item_id, item)

        # Product Category item
        item = self.test_promotion_percentage.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "2_product_category"
        )
        item.write({"percent_price": 40})
        sale_order.action_apply_promotion()
        self.assertEqual(product_1_line.price_unit, 100)
        self.assertEqual(product_1_line.discount, 40)
        self.assertEqual(product_2_line.price_unit, 100)
        self.assertEqual(product_2_line.discount, 46)
        self.assertEqual(product_1_line.product_campaign_item_id, item)
        self.assertEqual(product_2_line.product_campaign_item_id, item)

        # Product Template Item
        item_1 = self.test_promotion_percentage.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "1_product"
            and item.product_tmpl_id == self.test_product_1.product_tmpl_id
        )
        item_1.write({"percent_price": 50})
        item_2 = self.test_promotion_percentage.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "1_product"
            and item.product_tmpl_id == self.test_product_2.product_tmpl_id
        )
        item_2.write({"percent_price": 50})
        sale_order.action_apply_promotion()
        self.assertEqual(product_1_line.price_unit, 100)
        self.assertEqual(product_1_line.discount, 50)
        self.assertEqual(product_2_line.price_unit, 100)
        self.assertEqual(product_2_line.discount, 55)
        self.assertEqual(product_1_line.product_campaign_item_id, item_1)
        self.assertEqual(product_2_line.product_campaign_item_id, item_2)

        # Product Variant Item
        item_1 = self.test_promotion_percentage.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "0_product_variant"
            and item.product_id == self.test_product_1
        )
        item_1.write({"percent_price": 60})
        item_2 = self.test_promotion_percentage.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "0_product_variant"
            and item.product_id == self.test_product_2
        )
        item_2.write({"percent_price": 60})
        sale_order.action_apply_promotion()
        self.assertEqual(product_1_line.price_unit, 100)
        self.assertEqual(product_1_line.discount, 60)
        self.assertEqual(product_2_line.price_unit, 100)
        self.assertEqual(product_2_line.discount, 64)
        self.assertEqual(product_1_line.product_campaign_item_id, item_1)
        self.assertEqual(product_2_line.product_campaign_item_id, item_2)

        # No promotion applied - Recompute pricelist price
        item = self.test_promotion_percentage.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "3_global"
        )
        item.write({"percent_price": -50})

        item = self.test_promotion_percentage.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "2_product_category"
        )
        item.write({"percent_price": -50})
        item_1 = self.test_promotion_percentage.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "1_product"
            and item.product_tmpl_id == self.test_product_1.product_tmpl_id
        )
        item_1.write({"percent_price": -50})
        item_2 = self.test_promotion_percentage.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "1_product"
            and item.product_tmpl_id == self.test_product_2.product_tmpl_id
        )
        item_2.write({"percent_price": -50})
        item_1 = self.test_promotion_percentage.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "0_product_variant"
            and item.product_id == self.test_product_1
        )
        item_1.write({"percent_price": -50})
        item_2 = self.test_promotion_percentage.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "0_product_variant"
            and item.product_id == self.test_product_2
        )
        item_2.write({"percent_price": -50})
        self.test_pricelist_without_discount.item_ids.filtered(
            lambda item: item.product_id == self.test_product_1
        ).write(
            {
                "fixed_price": 20,
            }
        )
        self.test_pricelist_without_discount.item_ids.filtered(
            lambda item: item.product_id == self.test_product_2
        ).write(
            {
                "percent_price": 80,
            }
        )
        sale_order.action_apply_promotion()
        self.assertEqual(product_1_line.price_unit, 100)
        self.assertEqual(product_1_line.discount, 80)
        self.assertEqual(product_2_line.price_unit, 100)
        self.assertEqual(product_2_line.discount, 80)
        self.assertFalse(product_1_line.product_campaign_item_id)
        self.assertFalse(product_2_line.product_campaign_item_id)

        # Manually changed price/discount. Keep price/discount
        product_1_line.write({"price_unit": 100, "discount": 90})
        product_2_line.write({"price_unit": 100, "discount": 90})
        sale_order.action_apply_promotion()
        self.assertEqual(product_1_line.price_unit, 100)
        self.assertEqual(product_1_line.discount, 90)
        self.assertEqual(product_2_line.discount, 90)
        self.assertEqual(product_2_line.price_unit, 100)
        self.assertFalse(product_1_line.product_campaign_item_id)
        self.assertFalse(product_2_line.product_campaign_item_id)

    def test_min_qty_promotion(self):
        sale_order = self.sale_promotion_sale_order(self.test_pricelist_with_discount)
        order_line = sale_order.order_line[0]
        item = self.test_promotion_fixed_price.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "3_global"
        )
        item.write({"fixed_price": 90, "min_quantity": 2})
        sale_order.action_apply_promotion()
        self.assertEqual(order_line.price_unit, 100)
        self.assertFalse(order_line.product_campaign_id)
        sale_order.order_line[0].write({"product_uom_qty": 2})
        sale_order.action_apply_promotion()
        self.assertEqual(order_line.price_unit, 90)
        self.assertEqual(order_line.product_campaign_id, item.product_campaign_id)

    def test_campaign_date_general_promotion(self):
        sale_order = self.sale_promotion_sale_order(self.test_pricelist_with_discount)
        order_line = sale_order.order_line[0]
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
                "start_date": sale_order.date_order + timedelta(days=1),
                "end_date": sale_order.date_order + timedelta(days=2),
            }
        )
        sale_order.action_apply_promotion()
        self.assertEqual(order_line.price_unit, 100)
        self.assertFalse(order_line.product_campaign_id)
        self.test_campaign.write(
            {
                "start_date": sale_order.date_order - timedelta(days=1),
                "end_date": sale_order.date_order + timedelta(days=2),
            }
        )
        sale_order.action_apply_promotion()
        self.assertEqual(order_line.price_unit, 90)
        self.assertEqual(order_line.product_campaign_id, item.product_campaign_id)

    def test_item_date_item_promotion(self):
        sale_order = self.sale_promotion_sale_order(self.test_pricelist_with_discount)
        order_line = sale_order.order_line[0]
        item = self.test_promotion_fixed_price.product_campaign_item_ids.filtered(
            lambda item: item.applied_on == "3_global"
        )
        item.write(
            {
                "fixed_price": 90,
                "date_start": sale_order.date_order + timedelta(days=1),
                "date_end": sale_order.date_order + timedelta(days=2),
            }
        )
        sale_order.action_apply_promotion()
        self.assertEqual(order_line.price_unit, 100)
        self.assertFalse(order_line.product_campaign_id)
        item.write(
            {
                "date_start": sale_order.date_order - timedelta(days=1),
                "date_end": sale_order.date_order + timedelta(days=2),
            }
        )
        sale_order.action_apply_promotion()
        self.assertEqual(order_line.price_unit, 90)
        self.assertEqual(order_line.product_campaign_id, item.product_campaign_id)
