import frappe
from frappe.tests.utils import FrappeTestCase


class TestMerchantRecord(FrappeTestCase):

    def setUp(self):
        if not frappe.db.exists("Merchant Category", "Test Category"):
            frappe.get_doc({
                "doctype": "Merchant Category",
                "category_name": "Test Category"
            }).insert()

    def test_naming_uses_merchant_id(self):
        """Record's name should equal its merchant_id, per the
        field:merchant_id naming rule."""
        doc = frappe.get_doc({
            "doctype": "Merchant Record",
            "merchant_name": "Test Merchant",
            "merchant_id": "TEST-0001",
            "category": "Test Category",
            "status": "Draft"
        }).insert()

        self.assertEqual(doc.name, "TEST-0001")

    def test_category_is_mandatory(self):
        """Saving without a category should raise a MandatoryError."""
        doc = frappe.get_doc({
            "doctype": "Merchant Record",
            "merchant_name": "No Category Merchant",
            "merchant_id": "TEST-0002",
            "status": "Draft"
        })
        self.assertRaises(frappe.MandatoryError, doc.insert)
