import frappe

def execute(filters=None):
    filters = filters or {}
    
    columns = get_columns()
    data = get_data(filters)
    
    return columns, data


def get_columns():
    return [
        {"label": "Exception", "fieldname": "name", "fieldtype": "Link", "options": "Validation Exception", "width": 150},
        {"label": "Merchant Record", "fieldname": "merchant_record", "fieldtype": "Link", "options": "Merchant Record", "width": 150},
        {"label": "Rule", "fieldname": "data_quality_rule", "fieldtype": "Link", "options": "Data Quality Rule", "width": 150},
        {"label": "Severity", "fieldname": "severity", "fieldtype": "Data", "width": 100},
        {"label": "Created On", "fieldname": "creation", "fieldtype": "Datetime", "width": 160},
        {"label": "Days Open", "fieldname": "days_open", "fieldtype": "Int", "width": 100},
    ]


def get_data(filters):
    # Base condition: only Open exceptions matter for "aging" —
    # Approved/Rejected ones are resolved, no longer "aging"
    conditions = "WHERE status = 'Open'"
    values = {}
    
    # Optional severity filter, passed in from the report's filter UI
    if filters.get("severity"):
        conditions += " AND severity = %(severity)s"
        values["severity"] = filters.get("severity")
    
    # DATEDIFF(NOW(), creation) calculates how many days old each record is —
    # this is the actual "aging" metric
    query = f"""
        SELECT
            name,
            merchant_record,
            data_quality_rule,
            severity,
            creation,
            DATEDIFF(NOW(), creation) AS days_open
        FROM `tabValidation Exception`
        {conditions}
        ORDER BY days_open DESC
    """
    
    return frappe.db.sql(query, values, as_dict=True)
