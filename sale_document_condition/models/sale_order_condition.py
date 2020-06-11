# Copyright 2020 Valentin Vinagre <valentin.vinagre@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrderCondition(models.Model):
    _name = "sale.order.condition"
    _description = "sale order document conditions"

    @api.model
    def _get_default(self):
        res = self.search_count([
            ('default', '=', True),
            ('company_id', '=', self.env.user.company_id.id)
        ]) > 0
        return not res

    name = fields.Char(
        string='Name',
        copy=False
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.user.company_id,
        required=True,
    )
    body_html = fields.Html(
        string='Body',
        translate=True,
        sanitize=False
    )
    default = fields.Boolean(
        string='Default',
        default=_get_default
    )

    @api.multi
    @api.constrains('default', 'company_id')
    def _check_default(self):
        for sel in self:
            if self.search_count([
                ('default', '=', True),
                ('company_id', '=', sel.company_id.id)
            ]) > 1:
                raise ValidationError(
                    _('Only can exist one default sale condition by company.')
                )

    @api.multi
    @api.constrains('name')
    def _check_name(self):
        for sel in self:
            if self.search_count([('name', '=', sel.name)]) > 1:
                raise ValidationError(
                    _('This Condition already exists.')
                )
