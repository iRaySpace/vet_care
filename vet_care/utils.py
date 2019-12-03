import math
from frappe.utils.data import today, date_diff


def calculate_age(dob):
    return math.floor(
        date_diff(today(), dob) / 365
    )