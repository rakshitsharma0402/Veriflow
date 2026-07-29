import frappe

@frappe.whitelist()
def get_exception_summary():
    """
    Whitelisted API method — callable via frappe.call() from client-side
    JS, or directly via URL: /api/method/veriflow.veriflow.api.get_exception_summary
    
    Returns a JSON-serializable dict summarizing Validation Exceptions
    by status and severity.
    """
    
    by_status = frappe.db.sql("""
        SELECT status, COUNT(*) as count
        FROM `tabValidation Exception`
        GROUP BY status
    """, as_dict=True)
    
    by_severity = frappe.db.sql("""
        SELECT severity, COUNT(*) as count
        FROM `tabValidation Exception`
        GROUP BY severity
    """, as_dict=True)
    
    total = frappe.db.count("Validation Exception")
    
    return {
        "total": total,
        "by_status": by_status,
        "by_severity": by_severity
    }
