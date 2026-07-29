import frappe

@frappe.whitelist()
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


@frappe.whitelist()

def escalate_aged_exceptions():
    """
    Scheduled daily — escalates Open Validation Exceptions that have
    been open longer than the configured aging threshold.
    """
    settings = frappe.get_single("Veriflow Settings")
    threshold = settings.aging_alert_threshold_days or 7

    aged_exceptions = frappe.db.sql("""
        SELECT name, merchant_record, data_quality_rule, severity,
               DATEDIFF(NOW(), creation) AS days_open
        FROM `tabValidation Exception`
        WHERE status = 'Open'
          AND severity != 'Critical'
          AND DATEDIFF(NOW(), creation) >= %(threshold)s
    """, {"threshold": threshold}, as_dict=True)

    escalated_names = []

    for exc in aged_exceptions:
        doc = frappe.get_doc("Validation Exception", exc.name)
        previous_severity = doc.severity
        doc.severity = "Critical"
        doc.save(ignore_permissions=True)

        frappe.get_doc({
            "doctype": "Audit Log",
            "validation_exception": doc.name,
            "action": "Status Changed",
            "performed_by": "Administrator",
            "previous_status": f"Severity: {previous_severity}",
            "new_status": "Severity: Critical (auto-escalated)",
            "comment": (
                f"Auto-escalated after {exc.days_open} days open "
                f"(threshold: {threshold})"
            ),
            "timestamp": frappe.utils.now_datetime()
        }).insert(ignore_permissions=True)
        escalated_names.append(doc.name)

    if escalated_names and settings.governance_contact_email:
        try:
            frappe.sendmail(
                recipients=[settings.governance_contact_email],
                subject=f"Veriflow: {len(escalated_names)} exception(s) auto-escalated",
                message=(
                    f"The following exceptions exceeded the "
                    f"{threshold}-day aging threshold and were "
                    f"escalated to Critical:<br><br>"
                    f"{'<br>'.join(escalated_names)}"
                )
            )
        except Exception as e:
            frappe.log_error(
                title="Veriflow escalation email failed",
                message=f"Could not send escalation email: {str(e)}"
            )

    frappe.db.commit()
    frappe.logger().info(
        f"Escalated {len(escalated_names)} Validation Exception(s) to Critical."
    )
    return len(escalated_names)
