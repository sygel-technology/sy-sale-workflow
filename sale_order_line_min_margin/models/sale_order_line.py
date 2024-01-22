# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    margin_percent = fields.Float(
        readonly=False
    )

    @api.onchange("margin_percent")
    def onchange_margin_percent(self):
        for sel in self.filtered(
            lambda a: a.product_id and a.margin_percent != 1
        ):
            self.env.context = dict(self.env.context)
            self.env.context.update({'do_not_compute_discount': True})
            price_without_disc = sel.purchase_price / (
                1 - sel.margin_percent
            )
            if sel.discount != 100:
                sel.price_unit = price_without_disc / (1 - sel.discount / 100)
            company = sel.company_id or self.env.company
            if company.apply_so_line_min_margin and sel.margin_percent < company.so_line_min_margin / 100:
                return {
                    'warning': {
                        'title': _("Margin Warning"),
                        'message': _("The minimum margin set in company is {}%".format(
                            company.so_line_min_margin
                        )),
                    }
                }

    @api.onchange("purchase_price")
    def onchange_purchase_price(self):
        for sel in self.filtered(
            lambda a: a.product_id
        ):
            self.env.context = dict(self.env.context)
            self.env.context.update({'do_not_compute': True})
            price_without_disc = sel.purchase_price / (
                1 - sel.margin_percent
            )
            if sel.discount != 100:
                sel.price_unit = price_without_disc / (1 - sel.discount / 100)
            self.env.context.update({'do_not_compute': False})

    @api.onchange('product_id', 'price_unit', 'product_uom', 'product_uom_qty', 'tax_id')
    def _onchange_discount(self):
        if not self.env.context.get("do_not_compute_discount"):
            super()._onchange_discount()
        self.env.context = dict(self.env.context)
        self.env.context.update({'do_not_compute_discount': False})

    def _compute_margin(self):
        if not self.env.context.get("do_not_compute"):
            super()._compute_margin()
