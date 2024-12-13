# Copyright 2022 Ángel García de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CrmClaim(models.Model):
    _inherit = "crm.claim"

    quotation_and_order_count = fields.Integer(
        compute="_compute_sale_data", string="Number of Quotations and Orders"
    )

    def _compute_sale_data(self):
        res = self.env["sale.order"].read_group(
            domain=[
                ("claim_id", "in", self.ids),
            ],
            fields=["claim_id"],
            groupby=["claim_id"],
            lazy=False,
        )
        unit_count_dict = {d["claim_id"][0]: d["__count"] for d in res}
        for claim in self:
            claim.quotation_and_order_count = unit_count_dict.get(claim.id, 0)

    def action_view_sales(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "sale.action_quotations_with_onboarding"
        )
        action["context"] = {
            "search_default_partner_id": self.partner_id.id,
            "default_partner_id": self.partner_id.id,
            "default_claim_id": self.id,
        }
        action["domain"] = [("claim_id", "=", self.id)]
        return action

    def action_new_quotation(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "crm_claim_sale.crm_claim_sale_action_quotations_new"
        )
        action["context"] = {
            "search_default_claim_id": self.id,
            "default_claim_id": self.id,
            "search_default_partner_id": self.partner_id.id,
            "default_partner_id": self.partner_id.id,
            "default_origin": self.name,
            "default_company_id": self.company_id.id or self.env.company.id,
        }
        if self.team_id:
            action["context"]["default_team_id"] = (self.team_id.id,)
        if self.user_id:
            action["context"]["default_user_id"] = self.user_id.id
        sale_type = self.env["sale.order.type"].search(
            [("default_claim", "=", True)], limit=1
        )
        if sale_type:
            action["context"]["default_type_id"] = sale_type.id
        return action
