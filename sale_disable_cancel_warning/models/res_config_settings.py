# Copyright 2023 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    disable_cancel_warning = fields.Boolean(
        string='Disable Cancel Warning',
        config_parameter='sale_disable_cancel_warning.disable_cancel_warning',
        default=True,
    )
