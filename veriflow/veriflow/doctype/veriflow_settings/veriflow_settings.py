# Copyright (c) 2026, Rakshit Sharma and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class VeriflowSettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		aging_alert_threshold_days: DF.Int
		auto_reject_stale_exceptions: DF.Check
		default_severity: DF.Literal["Warning", "Critical"]
		governance_contact_email: DF.Data | None
	# end: auto-generated types

	_DOCTYPE_NAME = "Veriflow Settings"
