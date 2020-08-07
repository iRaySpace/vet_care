import frappe
import json
from datetime import timedelta
from frappe import _
from frappe.utils import today, getdate, now
from frappe.custom.doctype.custom_field.custom_field import create_custom_field
from erpnext.accounts.doctype.sales_invoice.sales_invoice import get_bank_cash_account
from toolz import pluck, partial, compose, first, concat
from vet_care.utils import timedelta_to_default_format


@frappe.whitelist()
def get_pet_relations(pet):
    return compose(list, partial(pluck, 'customer'))(
        frappe.get_all(
            'Pet Relation',
            filters={'parent': pet},
            fields=['customer']
        )
    )


@frappe.whitelist()
def apply_core_overrides():
    frappe.db.sql("""
        UPDATE `tabDocField` 
        SET set_only_once = 0
        WHERE parent = 'Patient'
        AND fieldname = 'customer'
    """)
    frappe.db.sql("""
        UPDATE `tabDocType`
        SET autoname = 'VS-.#####'
        WHERE name = 'Vital Signs'
    """)
    frappe.db.commit()

    return True


@frappe.whitelist()
def make_invoice(dt, dn):
    sales_invoice = frappe.new_doc('Sales Invoice')

    template = frappe.get_value('Lab Test', dn, 'template')
    rate = frappe.get_value('Lab Test Template', template, 'lab_test_rate')

    sales_invoice.append('items', {
        'item_code': template,
        'qty': 1,
        'rate': rate,
        'reference_dt': dt,
        'reference_dn': dn
    })

    patient = frappe.get_value('Lab Test', dn, 'patient')
    customer = frappe.get_value('Patient', patient, 'customer')
    sales_invoice.update({
        'patient': patient,
        'customer': customer,
        'due_date': today()
    })

    sales_invoice.set_missing_values()

    return sales_invoice


@frappe.whitelist()
def make_invoice_for_encounter(dt, dn):
    sales_invoice = frappe.new_doc('Sales Invoice')

    practitioner = frappe.get_value('Patient Encounter', dn, 'practitioner')
    op_consulting_charge_item = frappe.get_value('Healthcare Practitioner', practitioner, 'op_consulting_charge_item')
    op_consulting_charge = frappe.db.get_value('Healthcare Practitioner', practitioner, 'op_consulting_charge')

    sales_invoice.append('items', {
        'item_code': op_consulting_charge_item,
        'qty': 1,
        'rate': op_consulting_charge,
        'reference_dt': dt,
        'reference_dn': dn
    })

    patient = frappe.get_value('Patient Encounter', dn, 'patient')
    customer = frappe.get_value('Patient', patient, 'customer')

    sales_invoice.update({
        'patient': patient,
        'customer': customer,
        'due_date': today()
    })

    sales_invoice.set_missing_values()

    return sales_invoice


# deprecated
@frappe.whitelist()
def get_medical_records(patient):
    return frappe.get_all(
        'Patient Medical Record',
        filters={'patient': patient},
        fields=['reference_doctype', 'reference_name', 'communication_date']
    )


@frappe.whitelist()
def save_invoice(items, patient, customer, **kwargs):
    items = json.loads(items)
    sales_person = kwargs.get('sales_person')
    existing_invoice = kwargs.get('existing_invoice')
    discount_amount = kwargs.get('discount_amount')

    pos_profile = frappe.db.get_single_value('Vetcare Settings', 'pos_profile')
    taxes_and_charges = frappe.db.get_value('POS Profile', pos_profile, 'taxes_and_charges')

    if not pos_profile:
        frappe.throw(_('Please set POS Profile under Vetcare Settings'))

    if not existing_invoice:
        sales_invoice = frappe.new_doc('Sales Invoice')
        sales_invoice.update({
            'patient': patient,
            'customer': customer,
            'due_date': today(),
            'pos_profile': pos_profile,
            'pb_sales_person': sales_person,
            'taxes_and_charges': taxes_and_charges
        })
    else:
        sales_invoice = frappe.get_doc('Sales Invoice', existing_invoice)
        sales_invoice.items = []

    for item in items:
        sales_invoice.append('items', {
            'item_code': item.get('item_code'),
            'qty': item.get('qty'),
            'rate': item.get('rate')
        })

    if discount_amount:
        sales_invoice.apply_discount_on = 'Grand Total'
        sales_invoice.discount_amount = float(discount_amount)

    sales_invoice.set_missing_values()
    sales_invoice.set_taxes()
    sales_invoice.save()

    return sales_invoice


@frappe.whitelist()
def pay_invoice(invoice, payments):
    def get_mode_of_payment(company, mop):
        data = get_bank_cash_account(mop.get('mode_of_payment'), company)
        return {
            'mode_of_payment': mop.get('mode_of_payment'),
            'amount': mop.get('amount'),
            'account': data.get('account'),
        }

    payments = json.loads(payments)

    invoice = frappe.get_doc('Sales Invoice', invoice)
    invoice.update({'is_pos': 1})

    get_mop_data = partial(get_mode_of_payment, invoice.company)
    payments = list(map(get_mop_data, payments))
    for payment in payments:
        invoice.append('payments', payment)

    invoice.save()
    invoice.submit()

    return invoice


@frappe.whitelist()
def get_clinical_history(patient, filter_length):
    """
    Patient's Clinical History is consist of:
    (1) Patient Activity
    (2) Sales Invoice Items

    Clinical History returns structurally:
    ('posting_date', 'description', 'price')
    """
    date_format = _get_date_format()

    def make_data(row):
        row['posting_date'] = row['posting_date'].strftime(date_format)
        return row

    filter_length = int(filter_length)

    clinical_history_items = frappe.db.sql("""
        (SELECT 
            si.name,
            si.posting_date,
            si.pb_sales_person as sales_person,
            CONCAT(
                'INVOICE: ',
                ROUND(si_item.qty, 2),
                ' x ',
                si_item.item_name,
                ' (',
                si_item.item_code,
                ')'
            ) AS description,
            ROUND(si_item.amount, 3) AS price,
            si_item.creation,
            'si' AS ref_type
        FROM `tabSales Invoice Item` si_item
        INNER JOIN `tabSales Invoice` si ON si.name = si_item.parent
        WHERE si.customer = %s AND si.docstatus = 1)
        UNION ALL
        (SELECT
            pa.name,
            pa.posting_date,
            pa.sales_person,
            CONCAT(
                UPPER(pa_item.activity_type),
                ': ',
                pa_item.description
            ) AS description,
            '' AS price,
            pa_item.creation,
            'pa' AS ref_type
        FROM `tabPatient Activity Item` pa_item
        INNER JOIN `tabPatient Activity` pa on pa.name = pa_item.parent
        WHERE pa.patient = %s)
        ORDER BY posting_date DESC
        LIMIT %s
    """, (frappe.get_value('Patient', patient, 'customer'), patient, filter_length), as_dict=True)

    _apply_sales_person(clinical_history_items)

    return list(map(make_data, clinical_history_items))


@frappe.whitelist()
def make_patient_activity(patient, activity_items, sales_person=None):
    activity_items = json.loads(activity_items)

    patient_activity = frappe.get_doc({
        'doctype': 'Patient Activity',
        'patient': patient,
        'sales_person': sales_person,
        'posting_date': today()
    })

    for activity_item in activity_items:
        patient_activity.append('items', {
            'activity_type': activity_item['activity_type'],
            'description': activity_item['description']
        })

    patient_activity.save()

    return patient_activity


@frappe.whitelist()
def make_vital_signs(patient, vital_signs):
    vital_signs = json.loads(vital_signs)
    vital_signs_doc = frappe.get_doc({
        'doctype': 'Vital Signs',
        'patient': patient,
        'signs_date': today(),
        'signs_time': now(),
        'temperature': vital_signs.get('temperature'),
        'pulse': vital_signs.get('pulse'),
        'respiratory_rate': vital_signs.get('respiratory_rate'),
        'vc_mucous_membrane': vital_signs.get('mucous_membrane'),
        'vc_capillary_refill_time': vital_signs.get('capillary_refill_time'),
        'weight': vital_signs.get('weight')
    })
    vital_signs_doc.save()
    vital_signs_doc.submit()
    return vital_signs_doc


@frappe.whitelist()
def get_invoice_items(invoice):
    return frappe.get_all(
        'Sales Invoice Item',
        filters={'parent': invoice},
        fields=['item_code', 'item_name', 'qty', 'rate', 'amount']
    )


@frappe.whitelist()
def save_to_patient(patient, data):
    data = json.loads(data)
    patient_doc = frappe.get_doc('Patient', patient)
    patient_doc.update(data)
    patient_doc.save()


@frappe.whitelist()
def make_patient(patient_data, owner):
    patient_data = json.loads(patient_data)

    patient_doc = frappe.new_doc('Patient')
    patient_doc.update(patient_data)
    patient_doc.append('vc_pet_relation', {
        'default': 1,
        'relation': 'Owner',
        'customer': owner
    })
    patient_doc.save()

    return patient_doc


@frappe.whitelist()
def get_first_animal_by_owner(owner):
    data = frappe.get_all('Patient', filters={'customer': owner})
    return first(data) if data else None


@frappe.whitelist()
# TODO: filter availables
def get_practitioner_schedules(practitioner, date):
    def schedule_times(week_date, practitioner_schedule):
        return _get_schedule_times(practitioner_schedule, week_date)

    data = compose(
        list,
        set,
        sorted,
        concat,
        partial(map, partial(schedule_times, getdate(date))),
        partial(map, lambda x: x.get('schedule')),
    )

    practitioner_schedules = data(
        frappe.get_all(
            'Practitioner Service Unit Schedule',
            filters={'parent': practitioner},
            fields=['schedule']
        )
    )

    existing_appointments = frappe.get_all(
        'Patient Booking',
        filters={
            'physician': practitioner,
            'appointment_date': date,
            'docstatus': 1
        },
        fields=['appointment_time', 'appointment_minutes']
    )

    def get_available_slots(taken_slots, practitioner_schedule):
        for taken_slot in taken_slots:
            appointment_minutes = taken_slot.get('appointment_minutes')
            appointment_time = taken_slot.get('appointment_time')
            appointment_time_end = appointment_time + timedelta(minutes=appointment_minutes)
            if appointment_time <= practitioner_schedule < appointment_time_end:
                return False
        return True

    available_slots = compose(
        list,
        partial(filter, partial(get_available_slots, existing_appointments))
    )

    return compose(
        list,
        partial(map, timedelta_to_default_format), sorted)(available_slots(practitioner_schedules))


@frappe.whitelist()
def apply_custom_fields():
    create_custom_field('Healthcare Practitioner', {
        'fieldname': 'vc_color',
        'label': 'Color',
        'insert_after': 'office_phone'
    })
    return True


@frappe.whitelist()
def get_no_appointment_type():
    appointment_type = frappe.db.get_single_value('Vetcare Settings', 'no_appointment_type')
    patient = frappe.db.get_single_value('Vetcare Settings', 'no_patient')
    return {
        'appointment_type': appointment_type,
        'patient': patient
    }


@frappe.whitelist()
def get_tax_rate():
    pos_profile = frappe.db.get_single_value('Vetcare Settings', 'pos_profile')
    taxes_and_charges = frappe.db.get_value('POS Profile', pos_profile, 'taxes_and_charges')
    sales_taxes_and_charges = frappe.db.get_all(
        'Sales Taxes and Charges',
        filters={'parent': taxes_and_charges},
        fields=['rate']
    )
    if not sales_taxes_and_charges:
        frappe.throw(_('Unable to get tax rate for {}. Please set the taxes and charges'.format(pos_profile)))
    return sales_taxes_and_charges[0].get('rate')


@frappe.whitelist()
def get_selling_price_list():
    pos_profile = frappe.db.get_single_value('Vetcare Settings', 'pos_profile')
    selling_price_list = frappe.db.get_value('POS Profile', pos_profile, 'selling_price_list')
    if not selling_price_list:
        frappe.throw(_('Please set selling price list'))
    return selling_price_list


@frappe.whitelist()
def get_item_rate(item_code, selling_price_list):
    return compose(
        first,
        partial(pluck, 'price_list_rate')
    )(
        frappe.get_all(
            'Item Price',
            filters={
                'item_code': item_code,
                'price_list': selling_price_list,
                'selling': 1
            },
            fields=['price_list_rate']
        )
    )


def _get_schedule_times(name, date):
    """
    Fetch all `from_time` from [Healthcare Schedule Time Slot]
    :param name: [Practitioner Schedule]
    :param date: [datetime.date]
    :return:
    """
    mapped_day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    time_slots = frappe.get_all(
        'Healthcare Schedule Time Slot',
        filters={'parent': name, 'day': mapped_day[date.weekday()]},
        fields=['from_time']
    )
    return list(map(lambda x: x.get('from_time'), time_slots))


# TODO: include also with Patient
def _get_sales_invoice_items(customer):
    return frappe.db.sql("""
        SELECT 
            si.posting_date,
            si_item.item_code,
            si_item.qty,
            si_item.amount
        FROM `tabSales Invoice Item` si_item
        INNER JOIN `tabSales Invoice` si ON si.name = si_item.parent
        WHERE si.customer = %s
    """,
        (customer,),
        as_dict=1,
    )


def _get_date_format():
    date_format = frappe.db.get_single_value('Vetcare Settings', 'date_format')
    format_codes = {
        'mm': '%m',
        'dd': '%d',
        'yy': '%y',
        'yyyy': '%Y'
    }
    for key, value in format_codes.items():
        date_format = date_format.replace(key, value)
    return date_format


def _apply_sales_person(history):
    sales_person_by_doc = {}
    for row in history:
        sales_person = row.get('sales_person')
        sales_person_name = sales_person_by_doc.get(sales_person)
        if sales_person and sales_person not in sales_person_by_doc:
            sales_person_name = frappe.get_value('Employee', sales_person, 'employee_name')
            sales_person_by_doc[sales_person] = sales_person_name
        if sales_person_name:
            row['description'] = row['description'] + f'\nSales Person: {sales_person_name} ({sales_person})'


def get_search_values(customer):
    fields = [
            "customer_name",
            "mobile_number",
            "mobile_number_2",
            "vc_office_phone",
            "vc_home_phone",
            "vc_cpr",
    ]
    join = compose(lambda x: ";".join(x), partial(filter, None))
    if isinstance(customer, str):
        values = frappe.db.get_value("Customer", customer, fields)
        return join(values)
    if isinstance(customer, object) and customer.__class__.__name__ == "Customer":
        values = [customer.get(x) for x in fields]
        return join(values)
