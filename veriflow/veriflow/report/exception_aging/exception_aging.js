frappe.query_reports["Exception Aging"] = {
	filters: [
		{
			"fieldname": "severity",
			"label": __("Severity"),
			"fieldtype": "Select",
			"options": "\nWarning\nCritical"
		}
	]
};
