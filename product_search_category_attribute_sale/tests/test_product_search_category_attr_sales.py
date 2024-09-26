# Copyright 2024 Sygel - Manuel Regidor
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestProductSearchCategoryAttrSale(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Create categories
        # CAT
        #     CAT-A
        #         CAT A-A
        #         CAT A-B
        #     CAT-B

        cls.cat = cls.env["product.category"].create(
            {"name": "Cat", "parent_id": False}
        )
        cls.cat_a = cls.env["product.category"].create(
            {"name": "Cat-A", "parent_id": cls.cat.id}
        )
        cls.cat_a_a = cls.env["product.category"].create(
            {"name": "Cat-A-A", "parent_id": cls.cat_a.id}
        )
        cls.cat_a_b = cls.env["product.category"].create(
            {"name": "Cat-A-B", "parent_id": cls.cat_a.id}
        )
        cls.cat_b = cls.env["product.category"].create(
            {"name": "Cat-B", "parent_id": cls.cat.id}
        )

        # Create attributes and their values
        # Attr-a
        #     Val-aA
        #     Val-aB
        # Attr-b
        #     Val-bA
        #     Val-bB
        # Attr-c
        #     Val-cA
        #     Val-cB
        # Attr-d
        #     Val-dA
        #     Val-dB
        # Attr-e
        #     Val-eA
        #     Val-eB
        # Attr-f
        #     Val-fA
        #     Val-fB

        for i in ["a", "b", "c", "d", "e", "f"]:
            attr = cls.env["product.attribute"].create(
                {
                    "name": f"Attr-{i}",
                    "value_ids": [
                        (0, 0, {"name": f"Val-{i}A"}),
                        (0, 0, {"name": f"Val-{i}B"}),
                    ],
                }
            )
            setattr(cls, f"attr_{i}", attr)

        # Create product templates and apply attributes to autocreate product variants
        # Product Template A -> 4 product variants
        #     Attr-a (2 possible values)
        #     Attr-b (2 possible values)
        # Product Template B -> 4 product variants
        #     Attr-c (2 possible values)
        #     Attr-d (2 possible values)
        # Product Template C -> 4 product variants
        #     Attr-e (2 possible values)
        #     Attr-f (2 possible values)

        cls.product_template_a = cls.env["product.template"].create(
            {
                "name": "Product Template A",
                "categ_id": cls.cat_a_a.id,
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": cls.attr_a.id,
                            "value_ids": [(6, 0, cls.attr_a.value_ids.ids)],
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "attribute_id": cls.attr_b.id,
                            "value_ids": [(6, 0, cls.attr_b.value_ids.ids)],
                        },
                    ),
                ],
            }
        )
        cls.product_template_b = cls.env["product.template"].create(
            {
                "name": "Product Template B",
                "categ_id": cls.cat_a_b.id,
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": cls.attr_c.id,
                            "value_ids": [(6, 0, cls.attr_c.value_ids.ids)],
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "attribute_id": cls.attr_d.id,
                            "value_ids": [(6, 0, cls.attr_d.value_ids.ids)],
                        },
                    ),
                ],
            }
        )
        cls.product_template_c = cls.env["product.template"].create(
            {
                "name": "Product Template C",
                "categ_id": cls.cat_b.id,
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": cls.attr_e.id,
                            "value_ids": [(6, 0, cls.attr_e.value_ids.ids)],
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "attribute_id": cls.attr_f.id,
                            "value_ids": [(6, 0, cls.attr_f.value_ids.ids)],
                        },
                    ),
                ],
            }
        )

        # Create a sale order
        cls.sale_order = cls.env["sale.order"].create(
            {"partner_id": cls.env.ref("base.res_partner_1").id}
        )
        # Create wizard
        cls.search_product_wizard = cls.env["product.search.cat.attr.sale"].create(
            {"sale_id": cls.sale_order.id}
        )

    def test_prodcut_search_category_attr_list(self):
        search_product_wizard = self.search_product_wizard

        # Add category "Cat" and check the attribute lines
        self.search_product_wizard.category_id = self.cat.id
        search_product_wizard.apply_category()
        self.assertEqual(search_product_wizard.applied_category, self.cat)
        self.assertEqual(len(search_product_wizard.applied_category_ids), 1)
        self.assertFalse(search_product_wizard.category_id)
        self.assertEqual(len(search_product_wizard.attribute_line_ids), 6)

        # Add category "Cat-A" and check the attribute lines
        search_product_wizard.category_id = self.cat_a.id
        search_product_wizard.apply_category()
        self.assertEqual(search_product_wizard.applied_category, self.cat_a)
        self.assertEqual(len(search_product_wizard.applied_category_ids), 2)
        self.assertFalse(search_product_wizard.category_id)
        # There are 4 possible attributes in Cat/CatA products
        self.assertEqual(len(search_product_wizard.attribute_line_ids), 4)

        # Add category "Cat-A-A" and check the attribute lines
        search_product_wizard.category_id = self.cat_a_a.id
        search_product_wizard.apply_category()
        self.assertEqual(search_product_wizard.applied_category, self.cat_a_a)
        self.assertEqual(len(search_product_wizard.applied_category_ids), 3)
        self.assertFalse(search_product_wizard.category_id)
        # There are 2 possible attributes in "Cat/Cat-A/Cat-A-A" products
        self.assertEqual(len(search_product_wizard.attribute_line_ids), 2)

        # Remove current category
        search_product_wizard.delete_category()
        self.assertFalse(search_product_wizard.category_id)
        self.assertFalse(search_product_wizard.applied_category)
        self.assertFalse(search_product_wizard.applied_category_ids)
        self.assertFalse(search_product_wizard.attribute_line_ids)

        # Add category "Cat" and "Cat-B"" and check the attribute lines
        search_product_wizard.category_id = self.cat.id
        search_product_wizard.apply_category()
        search_product_wizard.category_id = self.cat_b.id
        search_product_wizard.apply_category()
        self.assertEqual(search_product_wizard.applied_category, self.cat_b)
        self.assertEqual(len(search_product_wizard.applied_category_ids), 2)
        self.assertFalse(search_product_wizard.category_id)
        # There are 2 possible attributes in "Cat/Cat-B" products
        self.assertEqual(len(search_product_wizard.attribute_line_ids), 2)

    def test_prodcut_search_category_attr_products(self):
        search_product_wizard = self.search_product_wizard

        search_product_wizard.category_id = self.cat.id
        search_product_wizard.apply_category()
        search_product_wizard.search_products()
        # Find all products whose category depends on category "Cat"
        self.assertEqual(len(search_product_wizard.product_line_ids), 12)

        # Find the attribute line related to attribute "Attr-a"
        attr_a_line = search_product_wizard.attribute_line_ids.filtered(
            lambda a: a.attribute_id == self.attr_a
        )
        self.assertEqual(len(attr_a_line), 1)
        # Select an attribute value for the attribute line related to attribute "Attr-a"
        # Search the products
        attr_a_line.write(
            {
                "attribute_value_ids": [
                    (4, self.attr_a.value_ids.filtered(lambda a: a.name == "Val-aA").id)
                ]
            }
        )
        search_product_wizard.search_products()
        self.assertEqual(len(search_product_wizard.product_line_ids), 2)

        # Find the attribute line related to attribute "Attr-b"
        attr_b_line = search_product_wizard.attribute_line_ids.filtered(
            lambda a: a.attribute_id == self.attr_b
        )
        self.assertEqual(len(attr_b_line), 1)
        # Select an attribute value for the attribute line related to attribute "Attr-b"
        # Search the products
        attr_b_line.write(
            {
                "attribute_value_ids": [
                    (4, self.attr_b.value_ids.filtered(lambda a: a.name == "Val-bA").id)
                ]
            }
        )
        search_product_wizard.search_products()
        self.assertEqual(len(search_product_wizard.product_line_ids), 1)

    def test_prodcut_search_category_attr_add_to_order(self):
        search_product_wizard = self.search_product_wizard

        # Apply category "Cat" and find products
        search_product_wizard.category_id = self.cat.id
        search_product_wizard.apply_category()
        search_product_wizard.search_products()
        # Select the products lines for product variants of "Product Template C"
        products_template_c = search_product_wizard.product_line_ids.filtered(
            lambda a: a.product_id.product_tmpl_id == self.product_template_c
        )
        self.assertEqual(len(products_template_c), 4)
        # Introduce 2 units in all of the lines
        products_template_c.write({"quantity": 2.0})
        search_product_wizard.create_order_lines()
        # Only the products for which the quantity in the wizard line is
        # greater than 0 have lines in the sale order
        self.assertEqual(len(self.sale_order.order_line), len(products_template_c))
        # All the product lines have the quantity introduced in the wizard
        for line in self.sale_order.order_line:
            self.assertEqual(line.product_uom_qty, 2.0)
