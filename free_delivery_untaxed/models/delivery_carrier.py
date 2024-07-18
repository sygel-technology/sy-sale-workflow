# Copyright 2021 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, fields, models


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    use_amount_untaxed = fields.Boolean(string="Use amount untaxed")

    def rate_shipment(self, order):
        res = super().rate_shipment(order)
        if (
            self.free_over
            and self.use_amount_untaxed
            and hasattr(self, "%s_rate_shipment" % self.delivery_type)
        ):
            res = getattr(self, "%s_rate_shipment" % self.delivery_type)(order)
            res["price"] = float(res["price"]) * (1.0 + (self.margin / 100.0))
            res["carrier_price"] = res["price"]
            if (
                res["success"]
                and self.free_over
                and self.use_amount_untaxed
                and order._compute_amount_untaxed_without_delivery() >= self.amount
            ):
                res["warning_message"] = _(
                    "The shipping is free since the order untaxed amount exceeds %.2f."
                ) % (self.amount)
                res["price"] = 0.0
        return res
