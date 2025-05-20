# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    margin_percent = fields.Float(readonly=False)

    @api.onchange("margin_percent")
    def onchange_margin_percent(self):
        for sel in self:
            sel.price_unit = sel.purchase_price / (1 - sel.margin_percent)
            company = sel.company_id or self.env.company
            if (
                company.apply_so_line_min_margin
                and sel.margin_percent < company.so_line_min_margin / 100
            ):
                return {
                    "warning": {
                        "title": _("Margin Warning"),
                        "message": _(
                            "The minimum margin set in company is %(margin)s%%"
                        )
                        % {"margin": company.so_line_min_margin},
                    }
                }
