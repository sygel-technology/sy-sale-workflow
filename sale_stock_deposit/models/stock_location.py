# Copyright 2023 Valentin Vinagre <valentin.vinagre@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StockLocation(models.Model):
    _inherit = "stock.location"

    deposit_location = fields.Boolean(
        string="Is a Deposit Location?",
        default=False,
        help="Check this box to allow using this location to put deposit goods.",
    )
    partner_id = fields.Many2one(comodel_name="res.partner", string="Owner")

    @api.constrains("location_id", "partner_id", "deposit_location", "company_id")
    def _check_one_deposit_by_location_and_partner(self):
        for sel in self:
            warehouse_id = sel.warehouse_id.view_location_id
            res = self.search_count(
                [
                    ("id", "child_of", warehouse_id.id),
                    ("company_id", "=", sel.company_id.id),
                    ("partner_id", "=", sel.partner_id.id),
                    ("deposit_location", "=", True),
                ]
            )
            if res > 1:
                raise ValidationError(
                    _(
                        "There cannot be two Deposits with the same "
                        "Partner and Warehouse."
                    )
                )

    def action_view_stock_deposit_wizard(self):
        action = {
            "name": _("{} Status").format(self.name),
            "view_mode": "list",
            "view_id": self.env.ref("stock.view_stock_quant_tree").id,
            "res_model": "stock.quant",
            "type": "ir.actions.act_window",
            "domain": [("location_id", "=", self.id)],
        }
        return action
