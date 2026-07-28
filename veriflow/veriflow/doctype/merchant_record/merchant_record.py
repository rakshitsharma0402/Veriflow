# Copyright (c) 2026, Rakshit Sharma and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class MerchantRecord(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		bonus_rate: DF.Percent
		category: DF.Link
		last_validation_on: DF.Datetime | None
		merchant_id: DF.Data
		merchant_name: DF.Data
		source_system: DF.Literal["Batch Feed A", "Batch Feed B", "Manual Entry"]
		status: DF.Literal["Draft", "Validated", "Pending Review", "Rejected"]
	# end: auto-generated types

	_DOCTYPE_NAME = "Merchant Record"
