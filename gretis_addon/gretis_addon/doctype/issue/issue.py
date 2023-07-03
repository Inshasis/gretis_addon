# Copyright (c) 2023, Inshasis and contributors
# For license information, please see license.txt

import frappe

def after_insert(doc,method):
	# if doc.issue_type:
	if doc.assigned_to:
		issue = frappe.get_doc({
			"doctype":"User Permission",
			"user":doc.assigned_to,
			"allow":"Issue",
			"for_value":doc.name,
		})
		issue.insert(ignore_permissions=True)

def on_trash(doc, method):
    # removing User Permission
	frappe.db.delete('User Permission', {'for_value': doc.name})

	

