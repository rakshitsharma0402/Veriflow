# Copyright (c) 2026, Rakshit Sharma and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class DataQualityRule(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		allowed_values: DF.SmallText | None
		applies_to_field: DF.Literal["merchant_name", "merchant_id", "category", "bonus_rate", "source_system"]
		is_active: DF.Check
		max_value: DF.Float
		min_value: DF.Float
		rule_name: DF.Data
		rule_type: DF.Literal["Not Empty", "Range Check", "Allowed Values"]
		severity: DF.Literal["Warning", "Critical"]
	# end: auto-generated types

	_DOCTYPE_NAME = "Data Quality Rule"
