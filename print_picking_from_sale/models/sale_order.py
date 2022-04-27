# Copyright 2022 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    complete_picking_id = fields.Many2one(
        string="Picking",
        comodel_name="stock.picking",
        domain="[('id', 'in', picking_ids)]",
        help="The name of the selected picking will be shown "
        "in the Complete Picking document.This field takes "
        "precedence over 'Complete Picking Name', so "
        "if both have a value, this is the one that will "
        "be used."
    )
    complete_picking_name = fields.Char(
        string="Complete Picking Name",
        help="Write the name to be shown on the Complete "
        "Picking Document.  'Picking' field takes precedence "
        "over this field.",
    )
    