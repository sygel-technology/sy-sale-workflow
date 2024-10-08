# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.base_queued_notify.tests.common import TestQueuedNotifyCommon


class TestQueuedSaleNotify(TestQueuedNotifyCommon):
    def setUp(cls):
        super().setUp()
        cls._setUpCommon(
            type_model=cls.env["sale.order.type"],
            notificable_model=cls.env["sale.order"],
            relation_field_name="type_id",
            prefix="sale_",
        )

    def _create_queues(self):
        return self.notificable_record.action_confirm()

    def _get_notify_ids(self):
        return self.type_record._get_sale_notify_ids().values()

    def test_generated_queues(self):
        self.assert_generated_queues()

    def test_notifications(self):
        self.assert_notifications()
