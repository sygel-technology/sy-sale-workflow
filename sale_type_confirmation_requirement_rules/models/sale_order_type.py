# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleOrderTypology(models.Model):
    _name = "sale.order.type"
    _inherit = ["sale.order.type", "requirement.rule.type.mixin"]

    requirement_rule_ids = fields.Many2many(
        comodel_name="sale.order.requirement.rule",
        relation="sale_confirmation_requirement_rule_type_rel",
    )
