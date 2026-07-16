# # # Copyright (c) 2026, SSDolui and contributors
# # # For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CustomerAccount(Document):

    def after_insert(self):
        self.create_customers(
            doc_account="Doc Receivable",
            cc_account="cc Receivable"
        )

    def on_trash(self):
        self.delete_customers()

    def validate(self):

        existing = frappe.db.exists(
            "Customer Account",
            {
                "customer_name": self.customer_name,
                "name": ["!=", self.name]
            }
        )

        if existing:
            frappe.throw(
                f"Customer Name '{self.customer_name}' already exists."
            )

    def delete_customers(self):

        customers = [
            f"{self.customer_name} Doc",
            f"{self.customer_name} CC"
        ]

        frappe.flags.from_customer_account = True

        try:
            for customer in customers:
                if frappe.db.exists("Customer", customer):
                    frappe.delete_doc(
                        "Customer",
                        customer,
                        ignore_permissions=True,
                        force=True
                    )
        finally:
            frappe.flags.from_customer_account = False

    def create_customers(self, doc_account, cc_account):

        self.create_customer(
            customer_name=f"{self.customer_name} Doc",
            receivable_account_name=doc_account
        )

        self.create_customer(
            customer_name=f"{self.customer_name} CC",
            receivable_account_name=cc_account
        )

    def create_customer(self, customer_name, receivable_account_name):

        if frappe.db.exists("Customer", customer_name):
            return frappe.get_doc("Customer", customer_name)

        customer = frappe.get_doc({
            "doctype": "Customer",
            "customer_name": customer_name,
            "default_currency": "USD",
            "accounts": []
        })

        companies = frappe.get_all("Company", fields=["name"])

        for company in companies:

            account_id = frappe.db.get_value(
                "Account",
                {
                    "account_name": receivable_account_name,
                    "company": company.name
                },
                "name"
            )

            if account_id:
                customer.append("accounts", {
                    "company": company.name,
                    "account": account_id
                })

        frappe.flags.from_customer_account = True

        try:
            customer.insert(ignore_permissions=True)
        finally:
            frappe.flags.from_customer_account = False

        return customer