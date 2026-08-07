import frappe
from frappe.tests.utils import FrappeTestCase
from veriflow.veriflow.rule_engine import evaluate_all_records


class TestRuleEngine(FrappeTestCase):

    def setUp(self):
        if not frappe.db.exists("Merchant Category", "Test Category"):
            frappe.get_doc({
                "doctype": "Merchant Category",
                "category_name": "Test Category"
            }).insert()

        if not frappe.db.exists("Data Quality Rule", "Test Range Rule"):
            frappe.get_doc({
                "doctype": "Data Quality Rule",
                "rule_name": "Test Range Rule",
                "applies_to_field": "bonus_rate",
                "rule_type": "Range Check",
                "min_value": 0,
                "max_value": 10,
                "severity": "Warning",
                "is_active": 1
            }).insert()

        if not frappe.db.exists("Merchant Record", "TEST-RE-0001"):
            frappe.get_doc({
                "doctype": "Merchant Record",
                "merchant_name": "Rule Engine Test Merchant",
                "merchant_id": "TEST-RE-0001",
                "category": "Test Category",
                "bonus_rate": 25,  # deliberately out of range
                "status": "Draft"
            }).insert()

    def test_range_check_creates_exception(self):
        """A bonus_rate of 25 should trigger the Range Check rule."""
        evaluate_all_records()

        exists = frappe.db.exists("Validation Exception", {
            "merchant_record": "TEST-RE-0001",
            "data_quality_rule": "Test Range Rule",
            "status": "Open"
        })
        self.assertTrue(exists)

    def test_duplicate_exception_not_created(self):
        """Running the rule engine twice should not create two exceptions
        for the same record+rule violation."""
        evaluate_all_records()
        evaluate_all_records()

        count = frappe.db.count("Validation Exception", {
            "merchant_record": "TEST-RE-0001",
            "data_quality_rule": "Test Range Rule",
            "status": "Open"
        })
        self.assertEqual(count, 1)
