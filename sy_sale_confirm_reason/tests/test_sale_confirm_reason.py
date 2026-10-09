# Copyright 2026 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase


class TestSaleConfirmReason(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.company_with_confirm_reason = cls.env.company
        cls.company_with_confirm_reason.sale_confirm_reason = True
        cls.company_without_confirm_reason = cls.env["res.company"].create(
            {
                "name": "Company Without Confirmation Reason",
                "sale_confirm_reason": False,
            }
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Customer",
            }
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "list_price": 100.0,
            }
        )
        cls.reason = cls.env["sale.confirm.reason"].create(
            {
                "name": "Test Reason",
                "company_id": cls.company_with_confirm_reason.id,
            }
        )
        cls.reason_with_text = cls.env["sale.confirm.reason"].create(
            {
                "name": "Reason With Text",
                "company_id": cls.company_with_confirm_reason.id,
                "allow_manual_text": True,
            }
        )
        cls.reason_required_text = cls.env["sale.confirm.reason"].create(
            {
                "name": "Reason With Required Text",
                "company_id": cls.company_with_confirm_reason.id,
                "allow_manual_text": True,
                "manual_text_required": True,
            }
        )

    def _create_sale_order(self, company=None):
        company = company or self.company_with_confirm_reason
        return self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "company_id": company.id,
                "order_line": [
                    fields.Command.create(
                        {
                            "product_id": self.product.id,
                            "product_uom_qty": 1.0,
                            "price_unit": 100.0,
                        }
                    )
                ],
            }
        )

    def _create_wizard(self, orders, reason, details=False):
        return self.env["sale.confirm.reason.wizard"].create(
            {
                "order_ids": [fields.Command.set(orders.ids)],
                "reason_id": reason.id,
                "details": details,
            }
        )

    def test_confirm_with_existing_reason(self):
        order = self._create_sale_order()
        order.confirm_reason_id = self.reason
        result = order.action_confirm()
        self.assertTrue(result)
        self.assertEqual(order.state, "sale")
        self.assertEqual(order.confirm_reason_id, self.reason)

    def test_confirm_with_reason(self):
        order = self._create_sale_order()
        wizard = self._create_wizard(order, self.reason)
        wizard.action_confirm()
        self.assertEqual(order.confirm_reason_id, self.reason)
        self.assertFalse(order.confirm_reason_details)
        self.assertEqual(order.state, "sale")

    def test_confirm_with_reason_details(self):
        order = self._create_sale_order()
        wizard = self._create_wizard(
            order,
            self.reason_with_text,
            "<p>Test details</p>",
        )
        wizard.action_confirm()
        self.assertEqual(order.confirm_reason_id, self.reason_with_text)
        self.assertEqual(
            order.confirm_reason_details,
            "<p>Test details</p>",
        )
        self.assertEqual(order.state, "sale")

    def test_confirm_with_required_reason_details(self):
        order = self._create_sale_order()
        wizard = self._create_wizard(
            order,
            self.reason_required_text,
            "<p>Required details</p>",
        )
        wizard.action_confirm()
        self.assertEqual(
            order.confirm_reason_id,
            self.reason_required_text,
        )
        self.assertEqual(
            order.confirm_reason_details,
            "<p>Required details</p>",
        )
        self.assertEqual(order.state, "sale")

    def test_details_not_stored_when_manual_text_not_allowed(self):
        order = self._create_sale_order()
        wizard = self._create_wizard(
            order,
            self.reason,
            "<p>This should not be stored</p>",
        )
        wizard.action_confirm()
        self.assertEqual(order.confirm_reason_id, self.reason)
        self.assertFalse(order.confirm_reason_details)
        self.assertEqual(order.state, "sale")

    def test_copy_reason(self):
        copied_reason = self.reason.copy()
        self.assertEqual(
            copied_reason.name,
            "Test Reason (copy)",
        )
        self.assertNotEqual(copied_reason, self.reason)

    def test_action_open_confirm_reason_wizard(self):
        order = self._create_sale_order()
        result = order._action_open_confirm_reason_wizard()
        self.assertEqual(result["type"], "ir.actions.act_window")
        self.assertEqual(result["res_model"], "sale.confirm.reason.wizard")
        self.assertEqual(result["view_mode"], "form")
        self.assertEqual(result["target"], "new")
        self.assertEqual(
            result["context"]["default_order_ids"],
            [fields.Command.set(order.ids)],
        )

    def test_onchange_reason_keeps_details_when_allowed(self):
        wizard = self.env["sale.confirm.reason.wizard"].new(
            {
                "reason_id": self.reason_with_text.id,
                "details": "<p>Test details</p>",
            }
        )
        wizard._onchange_reason_id()
        self.assertEqual(wizard.details, "<p>Test details</p>")

    def test_onchange_reason_clears_details_when_not_allowed(self):
        wizard = self.env["sale.confirm.reason.wizard"].new(
            {
                "reason_id": self.reason.id,
                "details": "<p>Test details</p>",
            }
        )
        wizard._onchange_reason_id()
        self.assertFalse(wizard.details)

    def test_confirm_reason_required_by_company(self):
        order = self._create_sale_order()
        self.assertTrue(order._show_confirm_reason_wizard())
        result = order.action_confirm()
        self.assertEqual(order.state, "draft")
        self.assertEqual(
            result["res_model"],
            "sale.confirm.reason.wizard",
        )
        self.assertEqual(
            result["context"]["default_order_ids"],
            [fields.Command.set(order.ids)],
        )

    def test_confirm_reason_not_required_by_company(self):
        order = self._create_sale_order(company=self.company_without_confirm_reason)
        self.assertFalse(order._show_confirm_reason_wizard())
        order.action_confirm()
        self.assertEqual(order.state, "sale")
        self.assertFalse(order.confirm_reason_id)

    def test_mass_confirm_opens_wizard(self):
        orders = self._create_sale_order() | self._create_sale_order()
        result = orders.action_confirm()
        self.assertEqual(
            result["res_model"],
            "sale.confirm.reason.wizard",
        )
        self.assertEqual(
            result["context"]["default_order_ids"],
            [fields.Command.set(orders.ids)],
        )
        self.assertTrue(all(order.state == "draft" for order in orders))

    def test_mass_confirm_with_reason(self):
        orders = self._create_sale_order() | self._create_sale_order()
        wizard = self._create_wizard(orders, self.reason)
        wizard.action_confirm()
        for order in orders:
            self.assertEqual(order.state, "sale")
            self.assertEqual(order.confirm_reason_id, self.reason)
            self.assertFalse(order.confirm_reason_details)

    def test_mass_confirm_with_reason_details(self):
        orders = self._create_sale_order() | self._create_sale_order()
        wizard = self._create_wizard(
            orders,
            self.reason_with_text,
            "<p>Mass confirmation details</p>",
        )
        wizard.action_confirm()
        for order in orders:
            self.assertEqual(order.state, "sale")
            self.assertEqual(order.confirm_reason_id, self.reason_with_text)
            self.assertEqual(
                order.confirm_reason_details,
                "<p>Mass confirmation details</p>",
            )

    def test_required_details_missing(self):
        order = self._create_sale_order()
        wizard = self._create_wizard(order, self.reason_required_text)
        with self.assertRaises(ValidationError):
            wizard.action_confirm()
        self.assertEqual(order.state, "draft")
        self.assertFalse(order.confirm_reason_id)

    def test_confirm_reason_wrong_company(self):
        order = self._create_sale_order()
        other_reason = self.env["sale.confirm.reason"].create(
            {
                "name": "Other Company Reason",
                "company_id": self.company_without_confirm_reason.id,
            }
        )
        wizard = self._create_wizard(order, other_reason)
        with self.assertRaises(ValidationError):
            wizard.action_confirm()
        self.assertEqual(order.state, "draft")

    def test_mass_confirm_different_companies(self):
        orders = self._create_sale_order() | self._create_sale_order(
            company=self.company_without_confirm_reason
        )
        wizard = self._create_wizard(orders, self.reason)
        with self.assertRaises(ValidationError):
            wizard.action_confirm()
        self.assertTrue(all(order.state == "draft" for order in orders))

    def test_confirm_reason_bypass(self):
        order = self._create_sale_order()
        order.with_context(skip_sale_confirm_reason=True).action_confirm()
        self.assertEqual(order.state, "sale")
        self.assertFalse(order.confirm_reason_id)

    def test_mass_confirm_reason_bypass(self):
        orders = self._create_sale_order() | self._create_sale_order()
        orders.with_context(skip_sale_confirm_reason=True).action_confirm()
        self.assertTrue(all(order.state == "sale" for order in orders))
        self.assertTrue(all(not order.confirm_reason_id for order in orders))

    def test_same_reason_name_different_companies(self):
        reason = self.env["sale.confirm.reason"].create(
            {
                "name": self.reason.name,
                "company_id": self.company_without_confirm_reason.id,
            }
        )
        self.assertEqual(reason.name, self.reason.name)
        self.assertNotEqual(reason.company_id, self.reason.company_id)

    def test_required_details_empty_html(self):
        order = self._create_sale_order()
        wizard = self._create_wizard(
            order,
            self.reason_required_text,
            "<p><br></p>",
        )
        with self.assertRaises(ValidationError):
            wizard.action_confirm()
        self.assertEqual(order.state, "draft")
        self.assertFalse(order.confirm_reason_id)
