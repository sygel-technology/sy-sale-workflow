# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleOrderTypology(models.Model):
    _inherit = "sale.order.type"

    send_confirmation_mails = fields.Boolean(string="Send Confirmation Mails")
    so_mail_delay = fields.Integer(
        string="Email delay (in minutes)",
        default=60,
    )
    # mail.template
    # Las plantillas utilizadas tienen que tener en blanco
    # el campo partner_to
    so_mail_id = fields.Many2one(
        string="Sale Order Template",
        comodel_name="mail.template",
        domain="[('model_id.model', '=', 'sale.order')]",
    )
    picking_complete_due_mail_id = fields.Many2one(
        string="Picking Complete Freight due",
        comodel_name="mail.template",
        domain="[('model_id.model', '=', 'stock.picking')]",
    )
    picking_complete_paid_id = fields.Many2one(
        string="Picking Complete Freight Paid",
        comodel_name="mail.template",
        domain="[('model_id.model', '=', 'stock.picking')]",
    )

    # De momento no tenemos en cuenta los albaranes parciales
    # picking_partial_due_id = fields.Many2one(
    #     string="Picking Partial Freight due",
    #     comodel_name="mail.template"
    # )
    # picking_partial_paid_id = fields.Many2one(
    #     string="Picking Partial Freight Paid",
    #     comodel_name="mail.template"
    # )
