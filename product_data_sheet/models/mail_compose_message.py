# Copyright 2020 Valentin Vinagre <valentin.vinagre@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


def _reopen(self, res_id, model, context=None):
    # save original model in context, because selecting the list of available
    # templates requires a model in context
    context = dict(context or {}, default_model=model)
    return {'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': res_id,
            'res_model': self._name,
            'target': 'new',
            'context': context,
            }


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    check_add_product_data_sheets = fields.Boolean(
        string="check data sheets",
        compute="_compute_check_add_product_data_sheets"
    )

    @api.multi
    @api.depends('model', 'res_id')
    def _compute_check_add_product_data_sheets(self):
        for sel in self:
            sel.check_add_product_data_sheets =\
                sel.model == 'sale.order' and sel.res_id

    @api.multi
    def add_product_data_sheets(self):
        for sel in self.filtered(
           lambda x: x.model == 'sale.order' and x.res_id):
            sale_obj = self.env[sel.model].browse(sel.res_id)
            attachment_ids =\
                sale_obj.order_line.mapped('product_id.data_sheet_ids').ids
            if attachment_ids:
                sel.write({
                    'attachment_ids': [(4, id) for id in attachment_ids]
                })
            return _reopen(self, sel.id, sel.model, context=self._context)
