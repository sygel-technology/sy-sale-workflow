# Copyright 2023 Ángel García de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def copy(self, default=None):
        self.ensure_one()
        res = super().copy(default)
        if self.env.company.use_number_suffix_duplicate_so and\
            res.so_copy_origin_id and\
                res.so_copy_origin_id.state in ['sale', 'done']:
            name = res.name
            confirmed_prefix = res.type_id.confirmed_so_prefix_by_type
            draft_prefix = res.type_id.sequence_id.prefix
            if draft_prefix:
                draft_prefix = draft_prefix.split('%')[0]
            if confirmed_prefix and draft_prefix:
                name = name.replace(confirmed_prefix, draft_prefix, 1)
            res.name = name
        return res
