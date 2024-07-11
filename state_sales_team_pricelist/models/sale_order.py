# Copyright 2023 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange("partner_id", "team_id")
    def _onchange_partner_sales_team(self):
        domain = [
            "|",
            ("company_id", "=", False),
            ("company_id", "=", self.company_id.id),
        ]
        if self.partner_id and self.partner_id.state_id:
            domain += [
                "|",
                ("state_ids", "=", False),
                ("state_ids", "in", self.partner_id.state_id.id),
            ]
        if self.team_id:
            domain += [
                "|",
                ("team_ids", "=", False),
                ("team_ids", "in", self.team_id.id),
            ]
        return {"domain": {"pricelist_id": domain}}
