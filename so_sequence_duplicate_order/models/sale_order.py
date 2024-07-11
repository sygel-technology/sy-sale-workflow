# Copyright 2023 Ángel García de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    so_copy_origin_id = fields.Many2one(
        comodel_name="sale.order", string="SO Copy Origin"
    )

    def copy(self, default=None):
        self.ensure_one()
        if self.env.company.use_number_suffix_duplicate_so:
            if not default:
                default = {}
            name_origin = self.name
            origin_id = self.id
            origin = self.name
            if self.origin:
                origin = f"{self.origin}, {name_origin}"
            if self.so_copy_origin_id:
                name_origin = self.so_copy_origin_id.name
                origin_id = self.so_copy_origin_id.id
                origin = name_origin
                if self.so_copy_origin_id.origin:
                    origin = f"{self.so_copy_origin_id.origin}, {name_origin}"
            count = 2 + self.search_count([("so_copy_origin_id", "=", origin_id)])
            default.update(
                {
                    "so_copy_origin_id": origin_id,
                    "origin": origin,
                    "name": f"{name_origin}/{count}",
                }
            )
        return super().copy(default)
