# Copyright 2023 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


import logging
from contextlib import contextmanager

from odoo import api, models
from odoo.tools.safe_eval import safe_eval

_logger = logging.getLogger(__name__)


@contextmanager
def savepoint(cr):
    """Open a savepoint on the cursor, then yield.

    Warning: using this method, the exceptions are logged then discarded.
    """
    try:
        with cr.savepoint():
            yield
    except Exception:
        _logger.exception("Error during an automatic workflow action.")


class AutomaticWorkflowJob(models.Model):
    _inherit = "automatic.workflow.job"

    def _do_force_invoice_orders(self, sale, domain_filter):
        if not self.env["sale.order"].search_count(
            [("id", "=", sale.id)] + domain_filter
        ):
            return f"{sale.display_name} {sale} job bypassed"
        sale.write({"force_invoiced": True})
        return f"{sale.display_name} {sale} set to force invoice successfully"

    @api.model
    def _force_invoice_orders(self, order_filter):
        sale_obj = self.env["sale.order"]
        sales = sale_obj.search(order_filter)
        _logger.debug("Sale Orders force invoice: %s", sales.ids)
        for sale in sales:
            with savepoint(self.env.cr):
                self._do_force_invoice_orders(
                    sale.with_company(sale.company_id), order_filter
                )

    @api.model
    def run_with_workflow(self, sale_workflow):
        workflow_domain = [("workflow_process_id", "=", sale_workflow.id)]
        if sale_workflow.force_invoice:
            self._force_invoice_orders(
                safe_eval(sale_workflow.force_invoice_order_filter_id.domain)
                + workflow_domain
            )
        return super().run_with_workflow(sale_workflow)
