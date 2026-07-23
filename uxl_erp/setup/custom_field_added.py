# my_app/setup/custom_field_provisioner.py

import frappe

# =========================================================================
# CENTRAL REGISTRY FOR CUSTOM FIELDS
# =========================================================================
CUSTOM_FIELDS_REGISTRY = {
    "Item":[
        {
            "fieldname": "custom_print_name",
            "label": "Print Name",
            "fieldtype": "Data",
            "insert_after": "item_name",
            "reqd": 0,
        },

    ],
    # ~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~
    # ~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~
    "Sales Order":[
        {
            "fieldname": "custom_sc_no",
            "label": "SC No",
            "fieldtype": "Data",
            "insert_after": "naming_series",
            "reqd": 1,
        },
        {
            "fieldname": "custom_category",
            "label": "Category",
            "fieldtype": "Link",
            "options":"Item Group",
            "insert_after": "delivery_date",
            "reqd": 1,
        }

    ],
    # ~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~
    # ~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~
    "Sales Order Item": [
        {
            "fieldname": "custom_print_name",
            "label": "Print Name",
            "fieldtype": "Data",
            "insert_after": "item_name",
        },
        {
            "fieldname": "custom_rate",
            "label": "Rate",
            "fieldtype": "Float",
            "insert_after": "rate",
        },
        {
            "fieldname": "custom_currency",
            "label": "Currency",
            "fieldtype": "Link",
            "options": "Currency",
            "insert_after": "rate",
            "reqd": 1,
            "default": "USD"
        },
        {
            "fieldname": "custom_exge_rate",
            "label": "Exge Rate",
            "fieldtype": "Float",
            "insert_after": "rate",
            "default": 1
        },
        {
            "fieldname": "custom_amount",
            "label": "Amount",
            "fieldtype": "Float",
            "insert_after": "rate",
        },
        {
            "fieldname": "custom_sc_no",
            "label": "SC No",
            "fieldtype": "Data",
            "insert_after": "qty",
        }
    ],
    # ~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~
    # ~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~
    "Sales Invoice":[
        {
            "fieldname": "custom_inv_no",
            "label": "INV No",
            "fieldtype": "Data",
            "insert_after": "naming_series",
            "reqd": 1,
        },
        {
            "fieldname": "custom_category",
            "label": "Category",
            "fieldtype": "Link",
            "options":"Item Group",
            "insert_after": "posting_date",
            "reqd": 1,
        }

    ]
}
# ~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~
# ~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~
# VALID FIELD TYPES ACCORDING TO FRAPPE CORE SCHEMAS
VALID_FIELD_TYPES = {
    "Data", "Long Text", "Small Text", "Text", "Select", "Int", "Float", "Currency", 
    "Check", "Date", "Datetime", "Time", "Link", "Dynamic Link", "Attach", "Attach Image", 
    "Text Editor", "Code", "Password", "ReadOnly", "Table", "Table MultiSelect"
}

def notify_developer_of_failure(doctype: str, context: str, error_msg: str, traceback_str: str = "") -> None:
    """
    Guarantees an unmistakable visual alarm across the terminal, 
    standard outputs, and Frappe database tracking layers.
    """
    alert_title = f"CRITICAL MIGRATION ABORTED: {doctype} -> ({context})"
    
    # 1. High-visibility Terminal Output
    print("\n" + "=" * 80)
    print(f"\033[91m\033[1m[DEVELOPER ALERT] {alert_title}\033[0m")
    print(f"\033[93mReason:\033[0m {error_msg}")
    print("=" * 80 + "\n")
    
    # 2. Permanent DB Logging
    frappe.log_error(
        title=alert_title,
        message=f"Error Details: {error_msg}\n\nTraceback Context:\n{traceback_str}"
    )

def apply() -> None:
    """
    Harden-engineered runner to automatically generate structural field definitions.
    Runs inside isolated transactional checkpoints per DocType block.
    """
    # 1. LIFECYCLE GUARD: Gracefully step out if the framework is setting up base installation states
    if not frappe.db or not frappe.db.exists("DocType", "Custom Field"):
        print("\033[93m[SKIPPED] Custom Field Provisioner: Database schema engine is bootstrap loading.\033[0m")
        return

    print("\033[94m[STARTING] Validating and deploying custom fields schema pre-migration...\033[0m")

    for doctype, fields in CUSTOM_FIELDS_REGISTRY.items():
        # Isolated savepoint context per individual target DocType block
        try:
            # 2. VALIDATION CHECK: Skip cleanly if an app is missing or not installed yet on the target site instance
            if not frappe.db.exists("DocType", doctype):
                continue

            # Fetch fresh metadata configurations once to optimize iterations
            meta = frappe.get_meta(doctype, cached=False)
            fields_modified = False

            for config in fields:
                fieldname = config.get("fieldname")
                if not fieldname:
                    notify_developer_of_failure(doctype, "Config Check", "Found a definition completely missing a 'fieldname' parameter.")
                    continue

                # 3. SAFETY GUARD: Field type sanitization check
                fieldtype = config.get("fieldtype", "Data")
                if fieldtype not in VALID_FIELD_TYPES:
                    notify_developer_of_failure(
                        doctype, fieldname, 
                        f"Specified fieldtype '{fieldtype}' is completely unrecognized by the Frappe framework standard ecosystem."
                    )
                    continue

                # 4. DUPLICATION GUARD: Check meta snapshot and explicit tables to avoid indexing conflicts
                if meta.has_field(fieldname) or frappe.db.exists("Custom Field", {"dt": doctype, "fieldname": fieldname}):
                    continue

                # 5. INSERT_AFTER TARGET GUARD: Prevent position assignment loops if anchor field is missing
                insert_after = config.get("insert_after")
                if insert_after and not meta.has_field(insert_after):
                    # Warning for developer but handles fallback execution cleanly
                    print(f"\033[93m[WARNING] '{doctype}': Anchor field '{insert_after}' missing. Placing at bottom.\033[0m")
                    insert_after = None

                # Build Document Mapping Definitions cleanly
                cf = frappe.new_doc("Custom Field")
                cf.update({
                    "dt": doctype,
                    "fieldname": fieldname,
                    "label": config.get("label", fieldname.replace("_", " ").title()),
                    "fieldtype": fieldtype,
                    "insert_after": insert_after,
                    "options": config.get("options"),
                    "reqd": config.get("reqd", 0),
                    "read_only": config.get("read_only", 0),
                    "in_list_view": config.get("in_list_view", 0),
                    "columns": config.get("columns", 0),
                    "hidden": config.get("hidden", 0),
                    "default": config.get("default"),
                })
                
                cf.insert(ignore_permissions=True, ignore_if_duplicate=True)
                fields_modified = True
                print(f"\033[92m[PRE-MIGRATE] Field '{fieldname}' safely added to '{doctype}' table structural layout.\033[0m")

            # 6. TRANSACTION RESOLUTION: Finalize mutations explicitly on successful step completion
            if fields_modified:
                frappe.clear_cache(doctype=doctype)
                frappe.db.updatedb(doctype)
                frappe.db.commit() # Safely save changes for this DocType

        except Exception as e:
            # Roll back changes only for this failed DocType block to protect the rest of the tables
            frappe.db.rollback()
            notify_developer_of_failure(
                doctype=doctype, 
                context="Runtime Loop Panic", 
                error_msg=str(e), 
                traceback_str=frappe.get_traceback()
            )
            # Proceeding onto next item in loop without blocking the complete migration process cascade.
            continue

    print("\033[94m[COMPLETED] Pre-migration custom field schema checks finished.\033[0m")