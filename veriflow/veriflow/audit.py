import frappe

def log_status_change(doc, method):
    if not doc.has_value_changed("status"):
        return
    
    previous_doc = doc.get_doc_before_save()
    previous_status = previous_doc.status if previous_doc else "Unknown"
    
    if doc.status == "Approved":
        action = "Approved"
    elif doc.status == "Rejected":
        action = "Rejected"
    else:
        action = "Status Changed"
    
    # NEW: auto-fill reviewed_by if it's empty and the record has moved
    # out of Open — same logic as the client script, but server-side,
    # so it happens as part of the SAME save operation (no double round-trip)
    if not doc.reviewed_by and doc.status != "Open":
        doc.reviewed_by = frappe.session.user
        doc.db_set("reviewed_by", frappe.session.user, update_modified=False)
    
    audit_entry = frappe.get_doc({
        "doctype": "Audit Log",
        "validation_exception": doc.name,
        "action": action,
        "performed_by": frappe.session.user,
        "previous_status": previous_status,
        "new_status": doc.status,
        "comment": doc.review_comment or "",
        "timestamp": frappe.utils.now_datetime()
    })
    
    audit_entry.insert(ignore_permissions=True)
