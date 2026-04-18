import frappe


def get_context(context):
	context.boot = get_boot()
	return context


def get_boot():
	boot = frappe._dict()
	boot.csrf_token = frappe.sessions.get_csrf_token()
	return boot
