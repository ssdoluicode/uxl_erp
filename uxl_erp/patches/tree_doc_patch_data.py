import frappe
from frappe.utils.nestedset import rebuild_tree

def execute(*args, **kwargs):
    """
    Safely creates Item Group tree nodes and rebuilds bounds without triggering
     premature NestedSet loop validation errors.
    """
    tree_data = [
        {"name": "All Item Groups", "is_group": 1, "parent": None},
        {"name": "Trade Item", "is_group": 1, "parent": "All Item Groups"},
        {"name": "Plastics", "is_group": 1, "parent": "Trade Item"},
        {"name": "PVC Resin", "is_group": 0, "parent": "Plastics"},
    ]

    for item in tree_data:
        parent = item.get("parent")
        
        # 1. Ensure parent node exists and is explicitly flagged as a group
        if parent and frappe.db.exists("Item Group", parent):
            frappe.db.set_value("Item Group", parent, "is_group", 1, update_modified=False)

        # 2. Insert if missing
        if not frappe.db.exists("Item Group", item["name"]):
            doc = frappe.get_doc({
                "doctype": "Item Group",
                "item_group_name": item["name"],
                "is_group": item.get("is_group", 0),
                "parent_item_group": parent
            })
            # Ignore standard controller validations and tree checks during raw insertion
            doc.flags.ignore_permissions = True
            doc.flags.ignore_mandatory = True
            doc.flags.ignore_on_update = True
            doc.insert()
            frappe.logger().info(f"Inserted Item Group: {item['name']}")
            
        else:
            # 3. Update existing records directly via DB to bypass NestedSetRecursionError
            frappe.db.set_value(
                "Item Group", 
                item["name"], 
                {
                    "is_group": item.get("is_group", 0),
                    "parent_item_group": parent
                },
                update_modified=False
            )

    # 4. Rebuild all tree indices (lft & rgt boundaries) safely in one pass
    rebuild_tree("Item Group", "parent_item_group")
    
    frappe.db.commit()