# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models

from odoo.addons.queue_job.job import DONE


class Picking(models.Model):
    _inherit = "stock.picking"

    @api.multi
    def send_email_to_client(self):
        for sel in self:
            mail_template = False
            # Buscamos el template del correo
            if sel.carrier_id.due_freight:
                mail_template = sel.sale_id.type_id.picking_complete_due_mail_id
            else:
                mail_template = sel.sale_id.type_id.picking_complete_paid_id
            if mail_template:
                mail_wizard = sel.env["mail.compose.message"].create(
                    {
                        "partner_ids": [(6, 0, [sel.sale_contact_id.id])],
                        "template_id": mail_template.id,
                    }
                )
                # No se ponen estos datos directamente porque da un error
                mail_wizard.update({"res_id": sel.id, "model": "stock.picking"})
                mail_wizard._get_composition_mode_selection()
                mail_wizard.onchange_template_id_wrapper()
                # Se elimina el correo de la dirección de envío si no tiene ninguno
                # asignado.
                if sel.partner_id.id in mail_wizard.partner_ids.ids and (
                    sel.partner_id.email is False or sel.partner_id.email == ""
                ):
                    mail_wizard.partner_ids = mail_wizard.partner_ids - sel.partner_id

                mail_wizard.with_context(avoid_followers=True).action_send_mail()

    def mark_so_queue_done(self, result):
        # Si el envío del mail de SO sigue en cola, se elimina
        self.sale_id.mail_queue_ids.filtered(
            lambda a: a.state not in ["done"]
        )._change_job_state(DONE, result)

    @api.multi
    def action_done(self):
        super(Picking, self).action_done()
        for sel in self.filtered(
            lambda a: a.picking_type_id.code == "outgoing"
            and a.sale_id
            and a.sale_contact_id.receive_confirmation_mails
            and a.sale_id.type_id.send_confirmation_mails
        ):
            sel.send_email_to_client()
            sel.mark_so_queue_done("Set to done by stock picking %s" % (sel.name))
