# Copyright 2023 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        ret_val = super().action_confirm()
        if ret_val:
            for order in self.filtered(
                lambda a: a.type_id
                and a.type_id.use_required_rules
                and a.type_id.required_rule_ids
            ):
                for rule in order.type_id.required_rule_ids:
                    domain = safe_eval(rule.domain) + [
                        ["id", "=", order.id],
                    ]
                    if self.search_count(domain) != 1:
                        raise ValidationError(rule.error_description)
        return ret_val
