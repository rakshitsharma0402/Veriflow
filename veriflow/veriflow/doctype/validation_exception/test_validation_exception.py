import frappe
from frappe.tests.utils import FrappeTestCase


class TestValidationException(FrappeTestCase):

    def setUp(self):
        if not frappe.db.exists("Merchant Category", "Test Category"):
            frappe.get_doc({
                "doctype": "Merchant Category",
                "category_name": "Test Category"
            }).insert()

        if not frappe.db.exists("Merchant Record", "TEST-VE-0001"):
            frappe.get_doc({
                "doctype": "Merchant Record",
                "merchant_name": "Audit Test Merchant",
                "merchant_id": "TEST-VE-0001",
                "category": "Test Category",
                "status": "Draft"
            }).insert()

        if not frappe.db.exists("Data Quality Rule", "Test Rule"):
            frappe.get_doc({
                "doctype": "Data Quality Rule",
                "rule_name": "Test Rule",
                "applies_to_field": "bonus_rate",
                "rule_type": "Range Check",
                "min_value": 0,
                "max_value": 10,
                "severity": "Warning",
                "is_active": 1
            }).insert()

    def test_audit_log_created_on_status_change(self):
        """Changing status should automatically create an Audit Log entry."""
        exc = frappe.get_doc({
            "doctype": "Validation Exception",
            "name": "TEST-VE-EXC-0001",
            "merchant_record": "TEST-VE-0001",
            "data_quality_rule": "Test Rule",
            "failure_reason": "Test failure",
            "severity": "Warning",
            "status": "Open"
        }).insert()

        before_count = frappe.db.count("Audit Log", {"validation_exception": exc.name})

        exc.status = "Approved"
        exc.save()

        after_count = frappe.db.count("Audit Log", {"validation_exception": exc.name})
        self.assertEqual(after_count, before_count + 1)

    def test_no_audit_log_when_status_unchanged(self):
        """Saving without changing status should NOT create a new Audit Log entry."""
        exc = frappe.get_doc({
            "doctype": "Validation Exception",
            "name": "TEST-VE-EXC-0002",
            "merchant_record": "TEST-VE-0001",
            "data_quality_rule": "Test Rule",
            "failure_reason": "Test failure",
            "severity": "Warning",
            "status": "Open"
        }).insert()

        before_count = frappe.db.count("Audit Log", {"validation_exception": exc.name})

        exc.failure_reason = "Updated reason, same status"
        exc.save()

        after_count = frappe.db.count("Audit Log", {"validation_exception": exc.name})
        self.assertEqual(after_count, before_count)
