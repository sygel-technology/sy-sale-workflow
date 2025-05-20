# Copyright 2023 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleOrderRequiredRule(models.Model):
    _name = "sale.order.required.rule"
    _description = "Sale Order Required Rule"

    name = fields.Char(required=True)
    domain = fields.Char(required=True, default="[]")
    error_description = fields.Text(required=True)
