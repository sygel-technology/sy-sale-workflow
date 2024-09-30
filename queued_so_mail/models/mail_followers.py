# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class Followers(models.Model):
    _inherit = "mail.followers"

    def _get_recipient_data(self, records, subtype_id, pids=None, cids=None):
        recipient_data = super(Followers, self)._get_recipient_data(
            records, subtype_id, pids, cids
        )
        if self.env.context.get("avoid_internal_users", False):
            delete_recipients = []
            for rep in recipient_data:
                if self.env["res.users"].search(
                    [("partner_id", "=", rep[0]), ("share", "=", False)], limit=1
                ):
                    delete_recipients.append(rep)
            for r in delete_recipients:
                recipient_data.remove(r)
        return recipient_data
