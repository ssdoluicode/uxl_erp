frappe.ui.form.on("Item", {
    item_name(frm) {
        if (!frm.doc.custom_print_name) {
            frm.set_value("custom_print_name", frm.doc.item_name);
        }
    }
});