# Copyright 2023 Angel Garcia de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    use_number_suffix_duplicate_so = fields.Boolean(
        string="Copy number suffix for duplicate sales orders",
        default=False
    )
