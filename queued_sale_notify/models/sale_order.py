# Copyright 2025 Valentin Vinagre <valentin.vinagre@sygel.es>
# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    mail_queue_ids = fields.Many2many(
        string="Mail Queues", comodel_name="queue.job", compute="_compute_mail_queues"
    )

    def action_confirm(self):
        res = super().action_confirm()
        notity_set = self.type_id._get_sale_notify_ids()
        for notify_ids in notity_set.values():
            for notify_id in notify_ids:
                for rec in self:
                    if notify_id.is_to_notify(rec):
                        notify_id.notify(rec)
        return res

    def _compute_mail_queues(self):
        for obj in self:
            obj.mail_queue_ids = (
                self.env["queue.job"]
                .search(
                    [
                        [
                            "func_string",
                            "=like",
                            f"sale.mail.notify(%,)._notify_thread(sale.order({obj.id},))",
                        ]
                    ]
                )
                .ids
            )
