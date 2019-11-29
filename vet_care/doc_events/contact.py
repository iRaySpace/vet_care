import frappe
import re

from frappe import _
from toolz import compose, partial, first


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
        partial(map, lambda x: x.phone)
    )(doc.phone_nos)

    if not valid_phone_numbers:
        frappe.throw(_('Phone numbers are not valid'))
