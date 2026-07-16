frappe.ui.form.on("Customer", {
    refresh(frm) {
        frm.set_df_property("customer_name", "read_only", 1);
    }
});

