
import frappe

def validate_create(doc, method):
    if frappe.flags.from_customer_account:
        return

    frappe.throw("Direct Customer creation is not allowed.")

def validate_delete(doc, method):
    if frappe.flags.from_customer_account:
        return

    frappe.throw("Delete from Customer Account only.")