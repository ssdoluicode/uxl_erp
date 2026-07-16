# Copyright (c) 2026, SSDolui and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ExportInvoice(Document):
	pass


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def address_query(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""
        SELECT DISTINCT dl.parent
        FROM `tabDynamic Link` dl
        WHERE dl.link_doctype = %(link_doctype)s
          AND dl.link_name = %(link_name)s
          AND dl.parent LIKE %(txt)s
        ORDER BY dl.parent
        LIMIT %(start)s, %(page_len)s
    """, {
        "link_doctype": filters.get("link_doctype"),
        "link_name": filters.get("link_name"),
        "txt": f"%{txt}%",
        "start": start,
        "page_len": page_len
    })

