/* Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
 *  * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

import {FormController} from "@web/views/form/form_controller";
import {patch} from "@web/core/utils/patch";
import {session} from "@web/session";

patch(FormController.prototype, {
    setup() {
        super.setup(...arguments);
        this._setSubViewLimitSale();
    },

    async _setSubViewLimitSale() {
        if (this.props.resModel === "sale.order") {
            const value = session.sale_order_line_display_number || 10000;
            const limit = parseInt(value, 10);
            var field = Object.values(this.archInfo.fieldNodes).find(
                (node) => node.name === "order_line"
            );
            if (field.views && field.views.list && limit) {
                field.views.list.limit = limit;
            }
        }
    },
});
