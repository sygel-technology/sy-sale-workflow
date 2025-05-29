# Copyright 2025 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleCampaign(models.Model):
    _name = "sale.campaign"
    _description = "Campaign"

    name = fields.Char(required=True)
    product_campaign_ids = fields.Many2many(
        comodel_name="product.campaign", string="Promotions"
    )
    start_date = fields.Date()
    end_date = fields.Date()
    pricelist_ids = fields.Many2many(
        comodel_name="product.pricelist", string="Pricelists"
    )
    active = fields.Boolean(default=True)
