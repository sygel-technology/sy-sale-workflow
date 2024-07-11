# Copyright 2023 Ángel García de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    deposit_count = fields.Integer(
        string="Deposits Counter", compute="_compute_deposit_count"
    )
    deposit_ids = fields.One2many(
        comodel_name="stock.location",
        inverse_name="partner_id",
        string="Stock Deposits",
    )

    def _compute_deposit_count(self):
        for sel in self:
            res = 0
            if sel.deposit_ids:
                res = len(sel.deposit_ids)
            sel.deposit_count = res

    def action_create_stock_deposit_wizard(self):
        result = self.env["ir.actions.act_window"]._for_xml_id(
            "sale_stock_deposit.res_partner_stock_deposit_creation_wizard_action"
        )
        result["context"] = dict(self.env.context, default_partner_id=self.id)
        return result

    def action_view_deposits(self):
        action = {
            "name": _("Deposits Status"),
            "view_mode": "list",
            "view_id": self.env.ref("stock.view_stock_quant_tree").id,
            "res_model": "stock.quant",
            "type": "ir.actions.act_window",
            "context": {"search_default_locationgroup": 1},
            "domain": [("location_id", "in", self.deposit_ids.ids)],
        }
        return action
