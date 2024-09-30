# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

from odoo.addons.queue_job.job import DONE, job


class SaleOrder(models.Model):
    _inherit = "sale.order"

    mail_queue_ids = fields.Many2many(
        string="Mail Queues", comodel_name="queue.job", compute="_compute_mail_queues"
    )
    has_queues = fields.Boolean(
        string="Has Queues", readonly=True, compute="_compute_has_queues"
    )

    @api.multi
    def _compute_mail_queues(self):
        for sel in self:
            all_queues = self.env["queue.job"].search(
                [
                    ("model_name", "=", "sale.order"),
                ]
            )
            sel.mail_queue_ids = all_queues.filtered(
                lambda a: sel.id in a.record_ids
            ).ids

    @api.depends("mail_queue_ids")
    def _compute_has_queues(self):
        for sel in self:
            sel.has_queues = True if sel.mail_queue_ids else False

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for sel in self.filtered(
            lambda a: a.partner_id.receive_confirmation_mails
            and a.type_id.send_confirmation_mails
            and a.type_id.so_mail_id
            and a.state in ("sale", "done")
        ):
            sel.with_delay(eta=sel.type_id.so_mail_delay * 60).delay_send_so_email()
        return res

    @job(default_channel="root.so_email")
    def delay_send_so_email(self):
        # Con el contexto indicamos que no queremos enviar correos a los
        # usuarios internos que están en la lista de followers.
        self.with_context(avoid_internal_users=True).message_post_with_template(
            self.type_id.so_mail_id.id
        )

    @api.multi
    def action_cancel(self):
        super(SaleOrder, self).action_cancel()
        for mail in self.mail_queue_ids.filtered(lambda a: a.state not in ["done"]):
            mail._change_job_state(DONE, "Set to done when SO was cancelled")
