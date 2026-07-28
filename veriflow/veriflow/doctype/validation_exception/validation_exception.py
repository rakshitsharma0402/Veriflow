# Copyright (c) 2026, Rakshit Sharma and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ValidationException(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		data_quality_rule: DF.Link
		failure_reason: DF.SmallText
		merchant_record: DF.Link
		review_comment: DF.SmallText | None
		reviewed_by: DF.Link | None
		reviewed_on: DF.Datetime | None
		severity: DF.Literal["Warning", "Critical"]
		status: DF.Literal["Open", "Approved", "Rejected"]
	# end: auto-generated types

	_DOCTYPE_NAME = "Validation Exception"
