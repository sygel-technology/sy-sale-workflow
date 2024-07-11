# Copyright 2023 Ángel García de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _action_confirm(self):
        for sel in self.filtered(lambda x: x.state in ["sale", "done"]):
            sel.name = sel._get_confirmed_order_sequence()
        return super()._action_confirm()

    def _get_confirmed_order_sequence(self):
        self.ensure_one()
        res = self.name
        if self.env.company.use_confirmed_prefix:
            sequence_ids = self.env["ir.sequence"].search(
                [
                    ("code", "=", "sale.order"),
                    ("company_id", "in", [self.env.company.id, False]),
                ],
                order="company_id",
            )
            if sequence_ids:
                prefix = sequence_ids[0].prefix
                if prefix:
                    prefix = prefix.split("%")[0]
                sequence = res.replace(prefix, "", 1) if prefix else res
                if sequence != res:
                    res = f"{self.env.company.confirmed_prefix}{sequence}"
        return res
