# Copyright 2023 Angel Garcia de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    use_number_suffix_duplicate_so = fields.Boolean(
        string="Copy number suffix for duplicate sales orders",
        related="company_id.use_number_suffix_duplicate_so",
        store=True,
        readonly=False
    )
