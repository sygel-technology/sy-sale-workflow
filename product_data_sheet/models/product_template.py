# Copyright 2020 Valentin Vinagre <valentin.vinagre@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    data_sheet_ids = fields.Many2many(
        'ir.attachment', 'product_data_sheet_attachment_rel',
        'product_id', 'attachment_id',
        string='Data Sheets',
    )
