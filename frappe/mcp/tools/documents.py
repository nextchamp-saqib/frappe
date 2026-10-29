# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE
"""Document tools reuse REST API v2 permissions and controller hooks."""

from typing import Any

from pydantic import Field

import frappe
from frappe import _
from frappe.api import v2
from frappe.mcp.tools import DocumentName, Tool, ToolArguments, form_dict
from frappe.model import child_table_fields, default_fields, optional_fields, table_fields

DocumentFields = list[str | dict[str, list[str]]] | None
WRITE_RESULT_FIELDS = ["name", "modified"]
FIELDS_DESCRIPTION = (
	'Fields to return. A table field as {"<table field>": ["<child field>", ...]}; "*" for all fields.'
)
WRITE_FIELDS_DESCRIPTION = FIELDS_DESCRIPTION + " Default: doctype, name and modified."
DATA_DESCRIPTION = (
	'Field values. A table field takes a list of rows, such as {"<table field>": [{"<child field>": ...}]}.'
)


class GetDocumentArguments(ToolArguments):
	doctype: str = Field(min_length=1)
	name: DocumentName
	fields: DocumentFields = Field(default=None, description=FIELDS_DESCRIPTION + " Default: all.")


class CountDocumentsArguments(ToolArguments):
	doctype: str = Field(min_length=1)
	filters: dict[str, Any] | list[Any] | None = None


class ListDocumentsArguments(ToolArguments):
	doctype: str = Field(min_length=1)
	filters: dict[str, Any] | list[Any] | None = None
	fields: list[str] | None = None
	order_by: str | None = None
	start: int = Field(default=0, ge=0)
	limit: int = Field(default=20, ge=1)


class CreateDocumentArguments(ToolArguments):
	doctype: str = Field(min_length=1)
	data: dict[str, Any] = Field(description=DATA_DESCRIPTION)
	fields: DocumentFields = Field(default=None, description=WRITE_FIELDS_DESCRIPTION)


class UpdateDocumentArguments(ToolArguments):
	doctype: str = Field(min_length=1)
	name: DocumentName
	data: dict[str, Any] = Field(
		description=DATA_DESCRIPTION
		+ " Rows sent for a table replace its rows: rows left out are deleted, a row with its name is updated."
	)
	fields: DocumentFields = Field(default=None, description=WRITE_FIELDS_DESCRIPTION)


class DeleteDocumentArguments(ToolArguments):
	doctype: str = Field(min_length=1)
	name: DocumentName


def get_document(doctype: str, name: str, fields: DocumentFields = None) -> dict:
	return document_fields(v2.read_doc(doctype, name), fields)


def count_documents(doctype: str, filters: dict[str, Any] | list[Any] | None = None) -> int:
	with form_dict({"filters": filters}):
		return v2.count(doctype)


def list_documents(
	doctype: str,
	filters: dict[str, Any] | list[Any] | None = None,
	fields: list[str] | None = None,
	order_by: str | None = None,
	start: int = 0,
	limit: int = 20,
) -> dict:
	arguments = {"filters": filters, "fields": fields, "order_by": order_by, "start": start, "limit": limit}
	with form_dict({key: value for key, value in arguments.items() if value is not None}):
		documents = v2.document_list(doctype)
		# The REST handler's pagination metadata belongs to its temporary response.
		has_next_page = bool(frappe.response.get("has_next_page"))
	return {"documents": documents, "has_next_page": has_next_page}


def create_document(doctype: str, data: dict[str, Any], fields: DocumentFields = None) -> dict:
	with form_dict(data):
		doc = v2.create_doc(doctype)
	return {"doctype": doc["doctype"], **document_fields(doc, fields or WRITE_RESULT_FIELDS)}


def update_document(doctype: str, name: str, data: dict[str, Any], fields: DocumentFields = None) -> dict:
	with form_dict(data):
		doc = v2.update_doc(doctype, name)
	return {"doctype": doc["doctype"], **document_fields(doc, fields or WRITE_RESULT_FIELDS)}


def delete_document(doctype: str, name: str) -> None:
	v2.delete_doc(doctype, name)


def document_fields(doc: dict, fields: DocumentFields = None) -> dict:
	"""Pick `fields` from a document dict, with JSON values parsed and nulls left out."""
	meta = frappe.get_meta(doc["doctype"])
	selected, child_fields = {}, {}
	for field in fields or ["*"]:
		if field == "*":
			selected.update(doc)
			continue
		for fieldname, child in field.items() if isinstance(field, dict) else ((field, None),):
			df = meta.get_field(fieldname)
			if child is not None and not (df and df.fieldtype in table_fields):
				frappe.throw(_("{0} is not a table field of {1}").format(fieldname, meta.name))
			if not df and fieldname not in (*default_fields, *optional_fields, *child_table_fields):
				frappe.throw(_("{0} is not a field of {1}").format(fieldname, meta.name))
			if fieldname in doc:
				selected[fieldname] = doc[fieldname]
				child_fields[fieldname] = child

	result = {}
	for fieldname, value in selected.items():
		if value is None:
			continue
		df = meta.get_field(fieldname)
		if df and df.fieldtype in table_fields:
			value = [document_fields(row, child_fields.get(fieldname)) for row in value]
		elif df and df.fieldtype == "JSON":
			value = frappe.parse_json(value)
		result[fieldname] = value
	return result


LIST_DOCUMENTS = Tool(
	name="list_documents",
	description="List documents like frappe.get_list.",
	arguments=ListDocumentsArguments,
	handler=list_documents,
	annotations={"readOnlyHint": True},
)

GET_DOCUMENT = Tool(
	name="get_document",
	description="Get one document with its child tables.",
	arguments=GetDocumentArguments,
	handler=get_document,
	annotations={"readOnlyHint": True},
)

COUNT_DOCUMENTS = Tool(
	name="count_documents",
	description="Count documents that match the filters, like list_documents.",
	arguments=CountDocumentsArguments,
	handler=count_documents,
	annotations={"readOnlyHint": True},
)

CREATE_DOCUMENT = Tool(
	name="create_document",
	description="Create a document with its child tables.",
	arguments=CreateDocumentArguments,
	handler=create_document,
	annotations={"destructiveHint": False},
)

UPDATE_DOCUMENT = Tool(
	name="update_document",
	description="Update fields of a document. Fields left out of data keep their values.",
	arguments=UpdateDocumentArguments,
	handler=update_document,
	annotations={"destructiveHint": True},
)

DELETE_DOCUMENT = Tool(
	name="delete_document",
	description="Delete a document.",
	arguments=DeleteDocumentArguments,
	handler=delete_document,
	annotations={"destructiveHint": True},
)
