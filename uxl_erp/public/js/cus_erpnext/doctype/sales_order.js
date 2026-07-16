frappe.ui.form.on("Sales Order", {
    setup(frm) {
        hide_fields(frm);
        set_default_values(frm);
   
    },

    onload(frm) {
        hide_fields(frm);
        set_default_values(frm);

    },
});

frappe.ui.form.on("Sales Order Item", {
    items_add(frm, cdt, cdn) {
        set_child_defaults(frm, cdt, cdn);
    },
    custom_currency(frm, cdt, cdn) {
        set_exchange_rate(frm, cdt, cdn);
    },
    item_code(frm, cdt, cdn) {
        set_exchange_rate(frm, cdt, cdn);
    },
    custom_rate(frm, cdt, cdn) {
        calculate_rate(cdt, cdn);
        calculate_custom_amount(cdt,cdn);
    },

    custom_exge_rate(frm, cdt, cdn) {
        calculate_rate(cdt, cdn);
    },
    qty(frm,cdt,cdn){
        calculate_custom_amount(cdt,cdn);
    }
});


// -------------------------------------------------------------------------------------------------------
// -------------------------------------------------------------------------------------------------------

const hide_fields_list = [
    "order_type", "currency_and_price_list", "scan_barcode", "set_warehouse"
];

const set_defaults = {
    "order_type":"Sales"
};

function hide_fields(frm) {
    hide_fields_list.forEach(field => {
        frm.set_df_property(field, "hidden", 1);
    });
}

function set_default_values(frm) {
    Object.entries(set_defaults).forEach(([field, value]) => {
        if (!frm.doc[field]) {
            frm.set_value(field, value);
        }
    });
}


const child_defaults = {
    "custom_currency": "USD"
};

function set_child_defaults(frm, cdt, cdn) {
    // Loop through the defaults and apply them ONLY to the specified row
    Object.entries(child_defaults).forEach(([field, value]) => {
        frappe.model.set_value(cdt, cdn, field, value);
    });
}

function set_exchange_rate(frm, cdt, cdn) {
    const row = locals[cdt][cdn];

    if (row.custom_currency === "USD") {
        frappe.model.set_value(cdt, cdn, "custom_exge_rate", 1);

        frm.fields_dict.items.grid.update_docfield_property(
            "custom_exge_rate",
            "read_only",
            1
        );
    } else {
        frm.fields_dict.items.grid.update_docfield_property(
            "custom_exge_rate",
            "read_only",
            0
        );
    }

    frm.refresh_field("items");
}

function set_exchange_rate(frm, cdt, cdn) {
    const row = locals[cdt][cdn];

    if (row.custom_currency === "USD") {
        frappe.model.set_value(cdt, cdn, "custom_exge_rate", 1);

        frm.fields_dict.items.grid.update_docfield_property(
            "custom_exge_rate",
            "read_only",
            1
        );
    } else {
        frm.fields_dict.items.grid.update_docfield_property(
            "custom_exge_rate",
            "read_only",
            0
        );
    }

    frm.refresh_field("items");
}

function calculate_rate(cdt, cdn) {
    const row = locals[cdt][cdn];

    if (row.custom_rate && row.custom_exge_rate) {
        frappe.model.set_value(
            cdt,
            cdn,
            "rate",
            flt(row.custom_rate) / flt(row.custom_exge_rate)
        );
    }
}
function calculate_custom_amount(cdt,cdn){
    const row = locals[cdt][cdn];

    if (row.qty && row.custom_rate){
       frappe.model.set_value(
        cdt, cdn, "custom_amount",
        row.qty * row.custom_rate
       )
    }

}
