# Copyright (c) 2026, Rakshit Sharma and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AuditLog(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		action: DF.Data | None
		comment: DF.SmallText | None
		new_status: DF.Data | None
		performed_by: DF.Data | None
		previous_status: DF.Data | None
		timestamp: DF.Datetime | None
		validation_exception: DF.Data | None
	# end: auto-generated types

	_DOCTYPE_NAME = "Audit Log"
