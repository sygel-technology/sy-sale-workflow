# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleOrderType(models.Model):
    _inherit = "sale.order.type"

    sale_mail_notify_ids = fields.One2many(
        name="Sale Mail Notifications",
        comodel_name="sale.mail.notify",
        inverse_name="sale_order_type_id",
    )
    sale_log_note_notify_ids = fields.One2many(
        name="Sale Log Note Notifications",
        comodel_name="sale.log.note.notify",
        inverse_name="sale_order_type_id",
    )
    sale_activity_notify_ids = fields.One2many(
        name="Sale Activity Notifications",
        comodel_name="sale.activity.notify",
        inverse_name="sale_order_type_id",
    )

    def _get_sale_notify_ids(self):
        return {
            "sale_mail_notify_ids": self.sale_mail_notify_ids,
            "sale_log_note_notify_ids": self.sale_log_note_notify_ids,
            "sale_activity_notify_ids": self.sale_activity_notify_ids,
        }
