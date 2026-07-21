

import json
import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

FORM_RULES = {
    
    "Sales Order": {
        "hide": [
            "order_type",
            "set_warehouse",
            "shipping_rule",
            "campaign",
            "source",
            "loyalty_points",
            "loyalty_amount",
            "coupon_code",
            "tc_name",
            "terms",
            "other_charges_calculation",
            "named_place"
        ],
        "defaults": {
            "order_type": "Sales",
        },
        "position":[
            {"fieldname": "incoterm", "after": "company"}
        ]
    },
    # ~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~
    # ~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~

    "Sales Order Item": {
      
        "grid_columns": [
            {"fieldname": "item_code", "size": 2},
            {"fieldname": "custom_print_name", "size": 2},
            {"fieldname": "qty", "size": 1},
            {"fieldname": "custom_rate", "size": 1},
            {"fieldname": "custom_amount", "size": 1},
            {"fieldname": "custom_currency", "size": 1},
            {"fieldname": "custom_exge_rate", "size": 1},
            {"fieldname": "amount", "size": 1}
        ]
    },

    # ~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~
    # ~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~
    "ITEM": {
        "hide": [
            "allow_alternative_item",
            "is_stock_item",
            "has_variants",
        ],
        "defaults": {
            "is_stock_item": 0,
        },
        # "position": [
        #     {"fieldname": "industry", "after": "language"},
        #     {"fieldname": "customer_type", "after": "customer_name"},
        # ],
    },

    # ~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~
    # ~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~
    "Customer": {
        "hide": [
            "territory",
            "lead_name",
            "account_manager",
        ],
        "defaults": {
            "customer_type": "Individual",
            "customer_group": "Individual",
        },
        "position": [
            {"fieldname": "industry", "after": "language"},
            {"fieldname": "customer_type", "after": "customer_name"},
        ],
    }
}

def log_error(doctype: str, context: str, message: str) -> None:
    """Logs the issue to Frappe's Error Log and prints a clear warning in the terminal."""
    title = f"Form Customization Alert: {doctype} ({context})"
    frappe.log_error(title=title, message=message)
    print(f"\033[91m[SKIPPED] {title}: {message}\033[0m")

def set_field_property_safe(doctype: str, fieldname: str, property_name: str, value, property_type: str) -> None:
    try:
        make_property_setter(
            doctype,
            fieldname,
            property_name,
            value,
            property_type,
            validate_fields_for_doctype=True,
        )
    except Exception as e:
        log_error(doctype, f"Field Property ({fieldname}:{property_name})", str(e))

def set_doctype_property_safe(doctype: str, property_name: str, value, property_type: str) -> None:
    try:
        make_property_setter(
            doctype,
            None,
            property_name,
            value,
            property_type,
            for_doctype=True,
            validate_fields_for_doctype=True,
        )
    except Exception as e:
        log_error(doctype, f"DocType Property ({property_name})", str(e))

def apply_positions_safe(doctype: str, positions: list[dict], meta) -> None:
    if not positions:
        return

    try:
        current_field_order = meta.get("field_order")
        if not current_field_order:
            current_field_order = [df.fieldname for df in meta.fields if df.fieldname]
        else:
            if isinstance(current_field_order, str):
                current_field_order = json.loads(current_field_order)

        field_order = list(current_field_order)

        for rule in positions:
            fieldname = rule.get("fieldname")
            after_fieldname = rule.get("after")
            before_fieldname = rule.get("before")

            if not fieldname:
                log_error(doctype, "Positioning", "Missing 'fieldname' key in rule configuration.")
                continue

            if bool(after_fieldname) == bool(before_fieldname):
                log_error(doctype, "Positioning", f"Field '{fieldname}' must specify exactly one of 'after' or 'before'.")
                continue

            target_fieldname = after_fieldname or before_fieldname

            if fieldname not in field_order:
                log_error(doctype, "Positioning", f"Source field '{fieldname}' not found in layout layout order.")
                continue

            if target_fieldname not in field_order:
                log_error(doctype, "Positioning", f"Anchor field '{target_fieldname}' not found in layout order.")
                continue

            if fieldname == target_fieldname:
                continue

            field_order.remove(fieldname)
            target_index = field_order.index(target_fieldname)

            if after_fieldname:
                target_index += 1

            field_order.insert(target_index, fieldname)

        set_doctype_property_safe(doctype, "field_order", json.dumps(field_order), "Text")

    except Exception as e:
        log_error(doctype, "Positioning Calculations Execution", str(e))

def apply() -> None:
    """Main safe deployment framework execution loop."""
    for doctype, rules in FORM_RULES.items():
        try:
            if not frappe.db.exists("DocType", doctype):
                continue

            meta = frappe.get_meta(doctype, cached=False)

            # 1. Process Hide Configs Safely
            for fieldname in rules.get("hide", []):
                if meta.has_field(fieldname):
                    set_field_property_safe(doctype, fieldname, "hidden", 1, "Check")
                else:
                    log_error(doctype, "Hide Configuration", f"Field '{fieldname}' does not exist on this site.")

            # 2. Process Defaults Configs Safely
            for fieldname, value in rules.get("defaults", {}).items():
                if meta.has_field(fieldname):
                    set_field_property_safe(doctype, fieldname, "default", str(value), "Data")
                else:
                    log_error(doctype, "Default Property Configuration", f"Field '{fieldname}' does not exist on this site.")

            # 3. Process Unified Grid View Column Sizing Configs Safely
            grid_columns = rules.get("grid_columns", [])
            if grid_columns:
                total_column_weight = 0
                valid_columns = []
                target_fieldnames = set()

                # Pass 1: Parse and sum calculate sizing limits
                for col in grid_columns:
                    fieldname = col.get("fieldname")
                    size = col.get("size", 1)

                    if not fieldname:
                        continue

                    if not meta.has_field(fieldname):
                        log_error(doctype, "Grid Layout Setup", f"Field '{fieldname}' does not exist on this site.")
                        continue

                    clean_size = max(1, int(size))
                    total_column_weight += clean_size
                    valid_columns.append((fieldname, clean_size))
                    target_fieldnames.add(fieldname)

                # Pass 2: Apply conditional execution rules if safe limit threshold matches
                if total_column_weight > 10:
                    log_error(
                        doctype,
                        "Column Limit Guard",
                        f"Combined grid layout sizing sum is {total_column_weight}. Max limit allowed is 10. Skipping grid updates."
                    )
                else:
                    # CLEAN SWEEP: Turn off default 'in_list_view' settings for any fields NOT listed in your config
                    for df in meta.fields:
                        if df.fieldname and df.fieldname not in target_fieldnames and df.in_list_view:
                            set_field_property_safe(doctype, df.fieldname, "in_list_view", 0, "Check")

                    # Pass 3: Set explicit column rules exclusively
                    for fieldname, clean_size in valid_columns:
                        set_field_property_safe(doctype, fieldname, "in_list_view", 1, "Check")
                        set_field_property_safe(doctype, fieldname, "columns", clean_size, "Int")

            # 4. Process Positions Layout Safely
            if "position" in rules:
                apply_positions_safe(doctype, rules["position"], meta)

            frappe.clear_cache(doctype=doctype)

        except Exception as e:
            log_error(doctype, "Critical Loop Runtime Failure", str(e))