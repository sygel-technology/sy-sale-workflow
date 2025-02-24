# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from unittest import mock

from odoo.tests.common import Form, TransactionCase

from odoo.addons.odoo_2_odoo_data_transfer.tests.test_odoo_2_odoo_data_transfer import (
    MockXMLRpcWrapper,
)


class TestOdoo2OdooSaleNoPicking(TransactionCase):
    def setUp(self):
        super().setUp()
        self.template_sale = self.env.ref("odoo_2_odoo_sale_no_picking.template_sale")
        self.template_sale_line = self.env.ref(
            "odoo_2_odoo_sale_no_picking.template_sale_line"
        )

    @mock.patch(
        "odoo.addons.odoo_2_odoo_data_transfer."
        "wizards.odoo_data_transfer_wizard.OdooXmlrpcWrapper"
    )
    def test_odoo_2_odoo_sale_no_picking(self, mock_class, *args):
        mock_class.side_effect = (
            lambda url, db, username, password, lang, archived: MockXMLRpcWrapper(
                url, db, username, password, lang, archived, env=self.env
            )
        )
        wiz_form = Form(self.env["odoo.data.transfer.wizard"])
        wiz_form.url = (
            wiz_form.db_name
        ) = wiz_form.db_user = wiz_form.db_password = "Foo"
        wiz_form.record_limit = 10
        wiz_form.template_id = self.template_sale
        wizard = wiz_form.save()
        wizard.action_validate()
        res = wizard.action_accept()
        log_id = self.env[res["res_model"]].browse(res["res_id"])
        self.assertFalse(
            any(
                order.picking_ids
                for order in log_id.transfered_records_ids.mapped("local_id")
            )
        )
