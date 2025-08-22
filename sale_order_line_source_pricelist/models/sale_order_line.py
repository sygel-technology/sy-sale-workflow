# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    source_pricelist_item_id = fields.Many2one(
        string="Source Pricelist Item",
        comodel_name="product.pricelist.item",
        compute="_compute_source_pricelist_item_id",
        store=True,
    )

    source_pricelist_id = fields.Many2one(
        string="Source Pricelist",
        comodel_name="product.pricelist",
        compute="_compute_source_pricelist_item_id",
        store=True,
    )

    # Calculate pricelist_item_id field recursively. This does not affect the price
    @api.depends(
        "pricelist_item_id",
        "order_id.pricelist_id",
        "product_id",
        "product_uom",
        "product_uom_qty",
    )
    def _compute_source_pricelist_item_id(self):
        for rec in self:
            item_id = rec.pricelist_item_id
            if item_id and item_id.base == "pricelist" and item_id.base_pricelist_id:
                item_id = item_id.get_recursive_item_id(
                    rec.product_id,
                    quantity=rec.product_uom_qty or 1.0,
                    uom=rec.product_uom,
                    date=rec._get_order_date(),
                )
            rec.source_pricelist_item_id = item_id
            rec.source_pricelist_id = item_id.pricelist_id
