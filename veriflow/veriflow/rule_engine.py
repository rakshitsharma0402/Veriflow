import frappe

def evaluate_all_records():
    """
    Scheduled function — checks every Merchant Record against every
    active Data Quality Rule, creating Validation Exceptions for any
    failures that don't already have an open exception.
    """
    active_rules = frappe.get_all(
        "Data Quality Rule",
        filters={"is_active": 1},
        fields=["name", "applies_to_field", "rule_type", "min_value", "max_value", "allowed_values", "severity"]
    )

    merchant_records = frappe.get_all(
        "Merchant Record",
        fields=["name", "merchant_name", "category", "bonus_rate", "source_system"]
    )

    created_count = 0

    for record in merchant_records:
        for rule in active_rules:
            field_value = record.get(rule.applies_to_field)
            failed = False
            reason = ""

            if rule.rule_type == "Not Empty":
                if not field_value:
                    failed = True
                    reason = f"{rule.applies_to_field} is empty"

            elif rule.rule_type == "Range Check":
                if field_value is not None and not (rule.min_value <= field_value <= rule.max_value):
                    failed = True
                    reason = f"{rule.applies_to_field} value {field_value} outside range {rule.min_value}-{rule.max_value}"

            elif rule.rule_type == "Allowed Values":
                allowed = [v.strip() for v in (rule.allowed_values or "").split(",")]
                if field_value not in allowed:
                    failed = True
                    reason = f"{rule.applies_to_field} value '{field_value}' not in allowed list"

            if failed:
                existing = frappe.db.exists("Validation Exception", {
                    "merchant_record": record.name,
                    "data_quality_rule": rule.name,
                    "status": "Open"
                })
                if not existing:
                    frappe.get_doc({
                        "doctype": "Validation Exception",
                        "name": f"VE-AUTO-{frappe.utils.random_string(8)}",
                        "merchant_record": record.name,
                        "data_quality_rule": rule.name,
                        "failure_reason": reason,
                        "severity": rule.severity,
                        "status": "Open"
                    }).insert(ignore_permissions=True)
                    created_count += 1

    frappe.db.commit()
    frappe.logger().info(f"Rule engine: created {created_count} new Validation Exceptions")
    return created_count
