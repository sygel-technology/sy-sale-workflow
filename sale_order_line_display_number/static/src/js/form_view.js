/* Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
 *  * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

odoo.define(
    "sale_order_line_display_number.sale_order_line_display_number",
    function (require) {
        "use strict";
        var FormView = require("web.FormView");
        var rpc = require("web.rpc");

        FormView.include({
            _setSubViewLimit: function (attrs) {
                this._super(attrs);
                if (
                    this.modelParams.modelName === "sale.order" &&
                    this.fieldsView.name === "sale.order.form"
                ) {
                    const limit = rpc
                        .query({
                            model: "ir.config_parameter",
                            method: "get_param",
                            args: ["sale_order_line_display_number.number"],
                        })
                        .then((res) => {
                            if (!_.isUndefined(res)) {
                                attrs.limit = parseInt(res);
                            }
                        });
                }
            },
        });
    }
);
