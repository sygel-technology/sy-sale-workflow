# Copyright 2024 Roger Sans <roger.sans@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    can_clone_sale_line = fields.Boolean(
        string="Can Clone Sale Order Line",
        default=True,
        compute="_compute_service_sale_line",
        store=True,
        readonly=False,
    )

    @api.depends("detailed_type")
    def _compute_service_sale_line(self):
        for record in self:
            record.can_clone_sale_line = record.detailed_type != "service"
