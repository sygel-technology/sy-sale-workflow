# Copyright 2023 Ángel García de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    workflow_process_id = fields.Many2one(
        compute="_compute_workflow_process_id",
        store=True,
        readonly=False,
    )

    @api.depends("type_id")
    def _compute_workflow_process_id(self):
        for sel in self:
            sel.workflow_process_id = sel.type_id.workflow_process_id
