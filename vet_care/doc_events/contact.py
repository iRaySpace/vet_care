import frappe
import re

from frappe import _
from toolz import compose, partial


def validate(doc, method):
    _validate_phone_nos(doc)


def _validate_phone_nos(doc):
    def phone_number(data):
        search = re.match(r'(^\+?)(.*)', data)
        return search.group(2)

    valid_phone_numbers = compose(
        all,
        partial(map, lambda x: x.isdigit()),
        partial(map, phone_number),
        partial(filter, lambda x: x),
        partial(map, lambda x: doc.get(x)),
    )(["phone", "mobile_no"])

    if not valid_phone_numbers:
        frappe.throw(_('Only phone numbers with + (plus sign) accepted'))
