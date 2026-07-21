import frappe
from erpnext.controllers.queries import item_query
from frappe.utils.nestedset import get_descendants_of

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def item_query_with_category(doctype, txt, searchfield, start, page_len, filters):
    filters = filters or {}
    
    # 1. Pop non-DocField keys so ERPNext doesn't turn them into bad SQL WHERE clauses
    category = filters.pop("custom_category", None)
   

    # 2. Build group list (Category + All Descendants)
    if category and frappe.db.exists("Item Group", category):
        child_groups = get_descendants_of("Item Group", category)
        group_names = [category] + child_groups
        
        # Safe array filter format for ERPNext report view
        filters["item_group"] = ["in", group_names]

    # 3. Call ERPNext's item_query passing company as a explicit kwarg
    return item_query(
        doctype=doctype,
        txt=txt,
        searchfield=searchfield,
        start=start,
        page_len=page_len,
        filters=filters,
    )