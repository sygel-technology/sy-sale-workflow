# Copyright 2022 Angel Garcia de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    monthly_invoicing = fields.Boolean(
        compute="get_monthly_invoicing",
        store=True,
        string="Automatic Monthly Invoicing",
    )

    @api.depends("partner_invoice_id")
    def get_monthly_invoicing(self):
        for order in self:
            order.monthly_invoicing = order.partner_invoice_id.monthly_invoicing

    def _create_invoices(self, grouped=False, final=False, date=None):
        if self.env.context.get("automatic_cron", False):
            order_groups = {}
            for order in self:
                group_key = [
                    order.company_id.id,
                    order.partner_invoice_id.id,
                    order.currency_id.id,
                    order.date_order.strftime("%m-%Y"),
                ]
                group_key = tuple(group_key)
                if group_key not in order_groups:
                    order_groups[group_key] = order
                else:
                    order_groups[group_key] += order
            moves = self.env["account.move"]
            for group in order_groups.values():
                moves += super(SaleOrder, group)._create_invoices(
                    grouped=grouped, final=final, date=date
                )
        else:
            moves = super()._create_invoices(grouped=grouped, final=final, date=date)
        return moves

    def create_monthly_invoices(self, validate=False):
        sales_to_invoices_ids = self.env["sale.order"].search(
            [
                (
                    "date_order",
                    ">=",
                    (datetime.now() - relativedelta(months=1)).replace(
                        day=1, hour=0, minute=0, second=0
                    ),
                ),
                (
                    "date_order",
                    "<",
                    (datetime.now()).replace(day=1, hour=0, minute=0, second=0),
                ),
                ("monthly_invoicing", "=", True),
                ("invoice_status", "=", "to invoice"),
            ]
        )
        moves = sales_to_invoices_ids.with_context(
            automatic_cron=True
        )._create_invoices()
        if validate:
            moves._post()
