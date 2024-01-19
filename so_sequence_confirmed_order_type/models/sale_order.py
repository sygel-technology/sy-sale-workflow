# Copyright 2023 Ángel García de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _get_confirmed_order_sequence(self):
        self.ensure_one()
        if self.type_id.use_confirmed_so_prefix_by_type and\
            self.type_id.sequence_id and\
                self.state in ['sale', 'done']:
            res = self.name
            prefix = self.type_id.sequence_id.prefix
            if prefix:
                prefix = prefix.split('%')[0]
            sequence = res.replace(prefix, '', 1) if prefix else res
            if sequence != res:
                res = "{}{}".format(
                    self.type_id.confirmed_so_prefix_by_type,
                    sequence
                )
        else:
            res = super()._get_confirmed_order_sequence()
        return res
