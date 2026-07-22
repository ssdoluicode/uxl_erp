import frappe
from frappe.utils.nestedset import rebuild_tree


def after_install():
    """Executed once when the app is installed."""
    try:
        create_item_group()
        frappe.logger().info("UXL ERP: Default Item Groups created successfully.")
    except Exception:
        frappe.log_error(
            title="UXL ERP - After Install",
            message=frappe.get_traceback()
        )
        raise


def create_item_group():
    """Create default Item Group tree if ERPNext is installed."""

    # Ensure ERPNext default root exists
    if not frappe.db.exists("Item Group", "All Item Groups"):
        frappe.logger().info(
            "UXL ERP: Skipping Item Group creation because 'All Item Groups' does not exist."
        )
        return

    tree_data = [
        {"name": "Trade Item", "is_group": 1, "parent": "All Item Groups"},
        {"name": "Plastics", "is_group": 1, "parent": "Trade Item"},
        {"name": "PVC Resin", "is_group": 0, "parent": "Plastics"},
    ]

    for item in tree_data:
        parent = item["parent"]

        # Ensure parent is marked as a group
        if parent and frappe.db.exists("Item Group", parent):
            frappe.db.set_value(
                "Item Group",
                parent,
                "is_group",
                1,
                update_modified=False,
            )

        if not frappe.db.exists("Item Group", item["name"]):
            frappe.get_doc({
                "doctype": "Item Group",
                "item_group_name": item["name"],
                "parent_item_group": parent,
                "is_group": item["is_group"],
            }).insert(
                ignore_permissions=True,
                ignore_if_duplicate=True,
            )

        else:
            frappe.db.set_value(
                "Item Group",
                item["name"],
                {
                    "parent_item_group": parent,
                    "is_group": item["is_group"],
                },
                update_modified=False,
            )

    # Rebuild Nested Set (lft/rgt)
    rebuild_tree("Item Group", "parent_item_group")