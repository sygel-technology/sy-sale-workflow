# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleNotifyMixin(models.AbstractModel):
    _name = "sale.notify.mixin"
    _description = "Mixin for queued sale notification events"

    _inherit = "notify.mixin"

    notified_model_name = "sale.order"

    trigger_state = fields.Selection(
        selection_add=[
            ("sale", "Confirmed Sales"),
        ],
        default="sale",
        required=True,
        ondelete={
            "sale": "cascade",
        },
    )

    sale_order_type_id = fields.Many2one(
        name="Sale Order Type", comodel_name="sale.order.type"
    )

    # TODO: Mover a private o borrarlo
    def is_to_notify(self, record):
        # Returns if a record is in a status to be notified
        return self.trigger_state == "sale" and record.state == "sale"
