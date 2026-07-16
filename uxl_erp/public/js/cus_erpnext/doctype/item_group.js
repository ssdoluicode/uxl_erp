frappe.ui.form.on("Item Group", {
    parent_item_group: function(frm) {
        // Ensure the parent field actually has a value before querying
        if (frm.doc.parent_item_group) {
            
            frappe.db.get_value('Item Group', frm.doc.parent_item_group, 'parent_item_group')
                .then(r => {
                    if (r && r.message) {
                        if (r.message.parent_item_group === "Trade Item") {
                            frm.set_value('is_group', 0);
                            frm.toggle_enable('is_group', false);
                        }else{
                            frm.toggle_enable('is_group', true);
                        }
                    }
                });
                
        }
    }
});