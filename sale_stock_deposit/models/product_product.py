# Copyright 2025 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _get_description(self, picking_type_id):
        description = super()._get_description(picking_type_id)
        if picking_type_id.code == "incoming":
            routes = (
                self.env["stock.route"]
                .search(
                    [
                        ("warehouse_id", "=", picking_type_id.warehouse_id.id),
                        ("deposit_operation", "=", True),
                        ("deposit_operation_type", "=", "deposit"),
                    ]
                )
                .filtered(
                    lambda route, type=picking_type_id: any(
                        rule.picking_type_id == type for rule in route.rule_ids
                    )
                )
            )
            if routes:
                description = self.description_pickingout or self.name
        return description
