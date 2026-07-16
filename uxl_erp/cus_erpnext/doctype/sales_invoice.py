import frappe
from frappe import _

def validate(doc, method):
    pro_cat= frappe.get_all("Item Group", filters= {"parent_item_group" : doc.custom_product_category}, pluck="item_group_name")
    for item in doc.items:
        item_group = frappe.db.get_value("Item", item.item_code, "item_group")
        if item_group not in pro_cat:
            frappe.throw(
                msg=_(f"Row #{item.idx}: Item {item.item_code} belongs to '{item_group}' group. Only items from {doc.custom_product_category} group are allowed!"),
                title=_("Validation Error")
            )