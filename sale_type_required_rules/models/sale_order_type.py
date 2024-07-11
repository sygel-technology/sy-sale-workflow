# Copyright 2023 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleOrderTypology(models.Model):
    _inherit = "sale.order.type"

    required_rule_ids = fields.Many2many(
        string="Order Required Rules", comodel_name="sale.order.required.rule"
    )
    use_required_rules = fields.Boolean(string="Use Required Rules")
