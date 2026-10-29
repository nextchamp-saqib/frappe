# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

from unittest.mock import patch

import frappe
from frappe.core.doctype.doctype.test_doctype import new_doctype
from frappe.desk.doctype.todo.todo import ToDo
from frappe.mcp.test_utils import McpTestCase


class TestGetDocuments(McpTestCase):
	def setUp(self):
		super().setUp()
		self.names = []
		for index in range(4):
			doc = frappe.get_doc(
				doctype="ToDo",
				description=f"MCP read fixture {index}",
				allocated_to=self.user if index < 3 else None,
			).insert()
			self.names.append(doc.name)
		self.filters = {"name": ["in", self.names]}

	def tearDown(self):
		try:
			frappe.set_user("Administrator")
			for name in self.names:
				frappe.delete_doc_if_exists("ToDo", name)
			# Requests use a second connection and publish the fixtures.
			frappe.db.commit()  # nosemgrep
		finally:
			super().tearDown()

	def read(self, *, tool="list_documents", **arguments):
		return self.request(
			{
				"jsonrpc": "2.0",
				"id": 1,
				"method": "tools/call",
				"params": {"name": tool, "arguments": arguments},
			}
		)

	def result(self, **arguments):
		response = self.read(**arguments)
		self.assertEqual(response.status_code, 200)
		self.assertFalse(response.json["result"]["isError"], response.json["result"])
		return response.json["result"]["structuredContent"]

	def test_named_read(self):
		result = self.result(tool="get_document", doctype="ToDo", name=self.names[0])
		self.assertEqual(result["name"], self.names[0])
		self.assertEqual(result["description"], "MCP read fixture 0")

	def test_named_read_denies_other_users_document(self):
		response = self.read(tool="get_document", doctype="ToDo", name=self.names[3])
		self.assertTrue(response.json["result"]["isError"])
		self.assertNotIn("structuredContent", response.json["result"])

	def test_list_and_count_hide_other_users_document(self):
		result = self.result(doctype="ToDo", filters=self.filters)
		self.assertEqual({row["name"] for row in result["documents"]}, set(self.names[:3]))
		self.assertEqual(
			self.result(doctype="ToDo", filters=self.filters, tool="count_documents")["result"], 3
		)

	def test_default_page_and_fields(self):
		result = self.result(doctype="ToDo", filters=self.filters)
		self.assertFalse(result["has_next_page"])
		self.assertEqual(set(result["documents"][0]), {"name"})

	def test_pagination_and_field_selection(self):
		first = self.result(
			doctype="ToDo",
			filters=self.filters,
			fields=["name", "description"],
			order_by="description asc",
			limit=2,
		)
		self.assertEqual(
			[row["description"] for row in first["documents"]], ["MCP read fixture 0", "MCP read fixture 1"]
		)
		self.assertTrue(first["has_next_page"])
		last = self.result(doctype="ToDo", filters=self.filters, order_by="description asc", start=2, limit=2)
		self.assertEqual([row["name"] for row in last["documents"]], [self.names[2]])
		self.assertFalse(last["has_next_page"])

	def test_operator_filters(self):
		result = self.result(doctype="ToDo", filters=[["name", "in", self.names[:2]]])
		self.assertEqual({row["name"] for row in result["documents"]}, set(self.names[:2]))
		self.assertEqual(
			self.result(doctype="ToDo", filters=[["name", "in", self.names[:2]]], tool="count_documents")[
				"result"
			],
			2,
		)

	def test_empty_results_and_count(self):
		filters = {"name": "MCP nonexistent document"}
		result = self.result(doctype="ToDo", filters=filters)
		self.assertEqual(result["documents"], [])
		self.assertFalse(result["has_next_page"])
		self.assertEqual(self.result(doctype="ToDo", filters=filters, tool="count_documents")["result"], 0)

	def test_no_mcp_page_size_cap(self):
		result = self.result(doctype="ToDo", filters=self.filters, limit=101)
		self.assertEqual(len(result["documents"]), 3)

	def test_missing_document_and_doctype(self):
		for arguments in (
			{"tool": "get_document", "doctype": "ToDo", "name": "MCP nonexistent document"},
			{"doctype": "MCP Nonexistent DocType"},
		):
			with self.subTest(arguments=arguments):
				self.assertTrue(self.read(**arguments).json["result"]["isError"])

	def test_doctype_permissions_are_checked_for_lists_and_counts(self):
		for tool in ("list_documents", "count_documents"):
			with self.subTest(tool=tool):
				response = self.read(doctype="OAuth Bearer Token", tool=tool)
				self.assertTrue(response.json["result"]["isError"])
				self.assertNotIn("structuredContent", response.json["result"])

	def test_field_permissions_on_named_read(self):
		result = self.result(tool="get_document", doctype="User", name=self.user)
		self.assertEqual(result["name"], self.user)
		self.assertIsNone(result.get("api_key"))
		self.assertIsNone(result.get("api_secret"))
		self.assertFalse(result.get("roles"))

	def test_invalid_arguments_never_execute_handler(self):
		cases = (
			{},
			{"doctype": 1},
			{"doctype": "ToDo", "limit": True},
			{"doctype": "ToDo", "limit": "20"},
			{"doctype": "ToDo", "limit": 0},
			{"doctype": "ToDo", "start": -1},
			{"doctype": "ToDo", "fields": [1]},
			{"doctype": "ToDo", "filters": "{}"},
			{"doctype": "ToDo", "count_only": "true"},
			{"doctype": "ToDo", "ignore_permissions": True},
			{"doctype": "ToDo", "name": self.names[0], "count_only": True},
		)
		with (
			patch("frappe.api.v2.read_doc") as read_doc,
			patch("frappe.api.v2.document_list") as document_list,
			patch("frappe.api.v2.count") as count,
		):
			for arguments in cases:
				with self.subTest(arguments=arguments):
					self.assertTrue(self.read(**arguments).json["result"]["isError"])
			read_doc.assert_not_called()
			document_list.assert_not_called()
			count.assert_not_called()

	def test_controller_list_hook_is_used(self):
		def get_list(query):
			self.assertEqual(frappe.session.user, self.user)
			return query.where(frappe.qb.DocType("ToDo").name == self.names[1])

		with patch.object(ToDo, "get_list", staticmethod(get_list), create=True):
			result = self.result(doctype="ToDo", filters=self.filters)
		self.assertEqual([row["name"] for row in result["documents"]], [self.names[1]])

	def test_mcp_matches_rest_list_and_count(self):
		arguments = {
			"filters": self.filters,
			"fields": ["name", "description"],
			"order_by": "description asc",
			"limit": 2,
		}
		mcp = self.result(doctype="ToDo", **arguments)
		rest = self.request(arguments, method="GET", path="/api/v2/document/ToDo")
		self.assertEqual(rest.status_code, 200)
		self.assertEqual(mcp["documents"], rest.json["data"])
		self.assertEqual(mcp["has_next_page"], rest.json["has_next_page"])
		mcp = self.result(doctype="ToDo", filters=self.filters, tool="count_documents")
		rest = self.request({"filters": self.filters}, method="GET", path="/api/v2/doctype/ToDo/count")
		self.assertEqual(rest.status_code, 200)
		self.assertEqual(mcp["result"], rest.json["data"])

	def test_field_permissions_on_lists(self):
		response = self.read(doctype="User", filters={"name": self.user}, fields=["name", "api_key"])
		self.assertFalse(response.json["result"]["isError"])
		self.assertEqual(len(response.json["result"]["structuredContent"]["documents"]), 1)
		keys = set(response.json["result"]["structuredContent"]["documents"][0])
		self.assertEqual(keys, {"name"})

	def test_exact_page_and_past_last_page(self):
		result = self.result(doctype="ToDo", filters=self.filters, limit=3)
		self.assertEqual(len(result["documents"]), 3)
		self.assertFalse(result["has_next_page"])
		result = self.result(doctype="ToDo", filters=self.filters, start=3)
		self.assertEqual(result["documents"], [])
		self.assertFalse(result["has_next_page"])


class TestDocumentFields(McpTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		if not frappe.db.exists("Role", "MCP Desk Tester"):
			frappe.get_doc(doctype="Role", role_name="MCP Desk Tester", desk_access=1).insert()
		values = [
			{"fieldname": "label", "fieldtype": "Data"},
			{"fieldname": "config", "fieldtype": "JSON"},
			{"fieldname": "note", "fieldtype": "Data"},
		]
		cls.child = new_doctype(fields=values, istable=1).insert().name
		cls.parent = (
			new_doctype(
				fields=[*values, {"fieldname": "rows", "fieldtype": "Table", "options": cls.child}],
				permissions=[{"role": "MCP Desk Tester", "read": 1, "write": 1, "create": 1}],
			)
			.insert()
			.name
		)
		frappe.db.commit()  # nosemgrep

	@classmethod
	def tearDownClass(cls):
		frappe.set_user("Administrator")
		frappe.delete_doc("DocType", cls.parent, force=True)
		frappe.delete_doc("DocType", cls.child, force=True)
		frappe.db.commit()  # nosemgrep
		super().tearDownClass()

	def setUp(self):
		super().setUp()
		self.name = (
			frappe.get_doc(
				doctype=self.parent,
				label="Parent",
				config={"limit": 10},
				rows=[{"label": "Row", "config": [1, 2]}],
			)
			.insert()
			.name
		)

	def call(self, tool, **arguments):
		return self.request(
			{
				"jsonrpc": "2.0",
				"id": 1,
				"method": "tools/call",
				"params": {"name": tool, "arguments": {"doctype": self.parent, **arguments}},
			}
		).json["result"]

	def result(self, tool="get_document", **arguments):
		result = self.call(tool, **arguments)
		self.assertFalse(result["isError"], result)
		return result["structuredContent"]

	def test_json_values_are_parsed_and_nulls_left_out(self):
		result = self.result(name=self.name)
		self.assertEqual(result["config"], {"limit": 10})
		self.assertNotIn("note", result)
		self.assertEqual(result["rows"][0]["config"], [1, 2])
		self.assertNotIn("note", result["rows"][0])
		self.assertNotIn(None, result["rows"][0].values())

	def test_fields_pick_document_and_table_fields(self):
		result = self.result(name=self.name, fields=["label", {"rows": ["label", "config"]}])
		self.assertEqual(result, {"label": "Parent", "rows": [{"label": "Row", "config": [1, 2]}]})
		result = self.result(name=self.name, fields=["name", "rows"])
		self.assertEqual(set(result), {"name", "rows"})
		self.assertEqual(result["rows"][0]["label"], "Row")

	def test_unknown_fields_are_rejected(self):
		for fields in (["lable"], [{"label": ["label"]}], [{"rows": ["lable"]}]):
			with self.subTest(fields=fields):
				result = self.call("get_document", name=self.name, fields=fields)
				self.assertTrue(result["isError"])
				self.assertIn("is not a", result["content"][0]["text"])

	def test_writes_return_name_and_modified(self):
		created = self.result("create_document", data={"label": "Created", "rows": [{"label": "Row"}]})
		self.assertEqual(set(created), {"doctype", "name", "modified"})
		self.assertEqual(created["doctype"], self.parent)
		updated = self.result("update_document", name=created["name"], data={"label": "Updated"})
		self.assertEqual(set(updated), {"doctype", "name", "modified"})
		self.assertEqual(
			updated["modified"], str(frappe.db.get_value(self.parent, created["name"], "modified"))
		)

	def test_writes_return_chosen_fields(self):
		result = self.result("update_document", name=self.name, data={"config": {"limit": 20}}, fields=["*"])
		self.assertEqual(result["config"], {"limit": 20})
		self.assertEqual(result["rows"][0]["config"], [1, 2])
		result = self.result("update_document", name=self.name, data={"label": "Updated"}, fields=["label"])
		self.assertEqual(result, {"doctype": self.parent, "label": "Updated"})
