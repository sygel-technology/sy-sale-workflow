# Copyright 2024 Ángel García de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
from odoo.tools import is_html_empty


class PickingType(models.Model):
    _inherit = "stock.picking.type"

    show_terms = fields.Boolean(
        string='Show Terms and Conditions'
    )


class Picking(models.Model):
    _inherit = "stock.picking"

    show_terms = fields.Boolean(
        string='Show Terms and Conditions',
        related='picking_type_id.show_terms'
    )
    stock_picking_terms = fields.Html( 
        string="Terms and Conditions Stock Picking",
        compute="_compute_stock_picking_terms",
        store=True,
        readonly=False,
    )

    @api.depends('partner_id')
    def _compute_stock_picking_terms(self):
        for sel in self:
            res = ""
            if sel.show_terms:
                sel = sel.with_company(sel.company_id)
                if not is_html_empty(self.env.company.stock_picking_terms):
                    res = sel.with_context(
                        lang=sel.partner_id.lang).env.company.stock_picking_terms
            sel.stock_picking_terms = res
