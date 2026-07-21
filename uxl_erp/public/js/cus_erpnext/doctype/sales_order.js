frappe.ui.form.on("Sales Order", {
    setup(frm) {
        hide_fields(frm);
        set_reqd(frm);
        calculate_delivery_date(frm);
        frm.set_df_property("company", "hidden", 0);

        
    },
    transaction_date(frm) {
        calculate_delivery_date(frm);
    },
    onload_post_render: function(frm) {
        frm.fields_dict['items'].grid.get_field('item_code').get_query = function(doc, cdt, cdn) {
            return {
                query: "uxl_erp.events.item_query.item_query_with_category",
                filters: {
                    "custom_category": doc.custom_category,
                    "customer": doc.customer,
                    "is_sales_item": 1
                }
            };
        };
    },
    onload(frm) {
        hide_fields(frm);
        // set_default_values(frm);
        frm.set_query("custom_category", function () {
            return {
                filters: {
                   parent_item_group: "Trade Item"
                }
            };
        });

    },
});

frappe.ui.form.on("Sales Order Item", {
    // items_add(frm, cdt, cdn) {
    //     set_child_defaults(frm, cdt, cdn);
    // },
    custom_currency(frm, cdt, cdn) {
        set_exchange_rate(frm, cdt, cdn);
    },
    item_code(frm, cdt, cdn) {
        set_exchange_rate(frm, cdt, cdn);

        const row = locals[cdt][cdn];

        if (row.item_code) {
            frappe.db.get_value("Item", row.item_code, "custom_print_name")
                .then(r => {
                    frappe.model.set_value(
                        cdt,
                        cdn,
                        "custom_print_name", // Replace with your actual fieldname
                        r.message.custom_print_name || ""
                    );
                });
        }
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
    "scan_barcode", "tax_category", "taxes_and_charges", "taxes", "total_taxes_and_charges"
];
const set_reqd_list = [
    "incoterm", "delivery_date"
]

const set_defaults = {
   
};
const child_defaults = {
   
};

// -------------------------------------------------------------------------------------------------------
// -------------------------------------------------------------------------------------------------------


function hide_fields(frm) {
    hide_fields_list.forEach(field => {
        frm.set_df_property(field, "hidden", 1);
    });
}
function set_reqd(frm) {
    set_reqd_list.forEach(field => {
        frm.set_df_property(field, "reqd", 1);
    });
}

function set_default_values(frm) {
    Object.entries(set_defaults).forEach(([field, value]) => {
        if (!frm.doc[field]) {
            frm.set_value(field, value);
        }
    });
}

function calculate_delivery_date(frm) {
    if (frm.doc.transaction_date) {
        // Safely add 30 days handling calendar changes cleanly
        let future_date = frappe.datetime.add_days(frm.doc.transaction_date, 30);
        
        // Apply the new value to the form field safely
        frm.set_value('delivery_date', future_date);
    }
}



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


