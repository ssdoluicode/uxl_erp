// Copyright (c) 2026, SSDolui and contributors
// For license information, please see license.txt

frappe.ui.form.on("Export Invoice", {
    refresh(frm) {
        frm.set_query("address", () => {
            return {
                query: "uxl_erp.uxl_custom.doctype.export_invoice.export_invoice.address_query",
                filters: {
                    link_doctype: "Customer Account",
                    link_name: frm.doc.customer
                }
            };
        });

    }
});
