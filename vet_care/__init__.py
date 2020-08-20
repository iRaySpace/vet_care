# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe

__version__ = '0.8.1'


def _get_jenv():
    import frappe

    if not getattr(frappe.local, 'jenv', None):
        from jinja2 import DebugUndefined
        from jinja2.sandbox import SandboxedEnvironment

        # frappe will be loaded last, so app templates will get precedence
        jenv = SandboxedEnvironment(loader=frappe.utils.jinja.get_jloader(),
                                    undefined=DebugUndefined)
        frappe.utils.jinja.set_filters(jenv)

        jenv.globals.update(frappe.utils.jinja.get_allowed_functions_for_jenv())
        jenv.globals.update(_get_jenv_customization('methods'))

        frappe.local.jenv = jenv

    return frappe.local.jenv


def _get_jenv_customization(customization_type):
    """Returns a dict with filter/method name as key and definition as value"""

    import frappe

    out = {}
    if not getattr(frappe.local, "site", None):
        return out

    values = frappe.get_hooks("jenv", {}).get(customization_type)
    if not values:
        return out

    for value in values:
        fn_name, fn_string = value.split(":")
        out[fn_name] = frappe.get_attr(fn_string)

    return out


frappe.utils.jinja.get_jenv = _get_jenv
