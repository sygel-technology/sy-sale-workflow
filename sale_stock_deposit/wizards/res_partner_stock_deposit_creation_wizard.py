# Copyright 2023 Ángel García de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class ResPartnerStockDepositCreationWizard(models.TransientModel):
    _name = "res.partner.stock.deposit.creation.wizard"
    _description = "Partner Stock Deposit Creation Wizard"

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner",
    )
    deposit_name = fields.Char(
        compute="_compute_deposit_name",
        readonly=False,
        required=True,
    )
    stock_deposit_id = fields.Many2one(
        comodel_name="stock.location",
        string="Location",
        domain="[('deposit_location', '=', True), ('partner_id', '=', False)]",
        required=True,
    )

    @api.depends("partner_id", "stock_deposit_id")
    def _compute_deposit_name(self):
        for sel in self:
            res = ""
            if sel.partner_id:
                res = _("Deposit {}").format(sel.partner_id.display_name)
                if sel.partner_id.ref:
                    res = _(
                        f"Deposit [{sel.partner_id.ref}] {sel.partner_id.display_name}"
                    )
            sel.deposit_name = res

    def action_create(self):
        self.env["stock.location"].sudo().create(
            {
                "name": self.deposit_name,
                "location_id": self.stock_deposit_id.id,
                "warehouse_id": self.stock_deposit_id.warehouse_id.id,
                "usage": "internal",
                "deposit_location": True,
                "partner_id": self.partner_id.id,
            }
        )
