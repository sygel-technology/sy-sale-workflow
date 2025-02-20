# Copyright 2025 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class OdooDataTransferWizard(models.TransientModel):
    _inherit = "odoo.data.transfer.wizard"

    def _create_record(self, record_dict):
        rec = super(
            OdooDataTransferWizard, self.with_context(skip_procurement=True)
        )._create_record(record_dict)
        return rec
