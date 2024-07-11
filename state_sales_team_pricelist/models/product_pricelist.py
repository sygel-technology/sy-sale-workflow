# Copyright 2023 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Pricelist(models.Model):
    _inherit = "product.pricelist"

    state_ids = fields.Many2many(comodel_name="res.country.state", string="States")
    team_ids = fields.Many2many(comodel_name="crm.team", string="Sales Teams")
