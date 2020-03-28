# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "vet_care"
app_title = "Vet Care"
app_publisher = "9T9IT"
app_description = "ERPNext App for Vet Care"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@9t9it.com"
app_license = "MIT"

fixtures = [
    {
        "doctype": "Custom Field",
        "filters": [
            [
                "name",
                "in",
                [
                    "Patient Appointment-vc_owner",
                    "Patient-vc_search_values",
                    "Patient-vc_species",
                    "Patient-vc_deceased",
                    "Patient-vc_breed",
                    "Patient-vc_chip_id",
                    "Patient-vc_weight",
                    "Vital Signs-vc_mucous_membrane",
                    "Vital Signs-vc_capillary_refill_time",
                    "Patient-vc_sb_relation",
                    "Patient-vc_pet_relation",
                    "Patient-vc_neutered",
                    "Inpatient Record-vc_customer",
                    "Patient-vc_color",
                    "Patient-vc_dtod",
                    "Patient-vc_rod",
                    "Patient-vc_nutrition",
                    "Sales Invoice-patient_name",
                    "Customer-vc_cpr",
                    "Customer-vc_cirrusvet",
                    "Patient-vc_cirrusvet",
                    "Customer-vc_address_and_contacts_sb",
                    "Customer-vc_flat_no",
                    "Customer-vc_building_no",
                    "Customer-vc_road_no",
                    "Customer-vc_road_name",
                    "Customer-vc_block_no",
                    "Customer-vc_city",
                    "Customer-vc_country",
                    "Customer-vc_address_and_contacts_cb",
                    "Customer-vc_home_phone",
                    "Customer-vc_office_phone",
                    "Customer-mobile_number",
                    "Customer-mobile_number_2",
                    "Customer-vc_area",
                    "Customer-vc_search_values",
                    "Healthcare Practitioner-vc_color",
                    "Patient-vc_inpatient",
                    "Healthcare Practitioner-vc_out_of_clinic"
                ]
            ]
        ]
    },
    {
        "doctype": "Property Setter",
        "filters": [
            [
                "name",
                "in",
                [
                    "Vital Signs-temperature-description",
                    "Vital Signs-pulse-description",
                    "Vital Signs-respiratory_rate-description",
                    "Vital Signs-reflexes-hidden",
                    "Vital Signs-bp_systolic-hidden",
                    "Vital Signs-bp_diastolic-hidden",
                    "Vital Signs-tongue-hidden",
                    "Vital Signs-abdomen-hidden",
                    "Patient-report_preference-hidden",
                    "Patient-mobile-read_only",
                    "Patient-email-hidden",
                    "Patient-phone-hidden",
                    "Patient-mobile-in_list_view",
                    "Patient-email-in_list_view",
                    "Patient-phone-in_list_view",
                    "Patient-sb_relation-hidden",
                    "Patient-patient_relation-hidden",
                    "Patient-customer-hidden",
                    "Patient-personal_and_social_history-hidden",
                    "Patient-occupation-hidden",
                    "Patient-column_break_25-hidden",
                    "Patient-marital_status-hidden",
                    "Patient-tobacco_past_use-hidden",
                    "Patient-tobacco_current_use-hidden",
                    "Patient-alcohol_past_use-hidden",
                    "Patient-alcohol_current_use-hidden",
                    "Patient-column_break_32-hidden",
                    "Patient-patient_name-unique",
                    "Patient-blood_group-hidden",
                    "Inpatient Record-mobile-hidden",
                    "Inpatient Record-email-hidden",
                    "Inpatient Record-phone-hidden",
                    "Inpatient Record-blood_group-hidden",
                    "Inpatient Record-expected_discharge-in_list_view",
                    "Inpatient Record-scheduled_date-in_list_view",
                    "Patient-surrounding_factors-label",
                    "Item-is_stock_item-default",
                    "Customer-search_fields",
                    "Vital Signs-nutrition_note-hidden",
                    "Vital Signs-bmi-hidden",
                    "Vital Signs-height-hidden",
                    "Customer-address_contacts-hidden",
                    "Customer-address_html-hidden",
                    "Customer-website-hidden",
                    "Customer-column_break1-hidden",
                    "Customer-contact_html-hidden",
                    "Customer-is_internal_customer-hidden",
                    "Customer-more_info-hidden",
                    "Customer-customer_details-hidden",
                    "Customer-column_break_45-hidden",
                    "Customer-market_segment-hidden",
                    "Customer-industry-hidden",
                    "Customer-is_frozen-hidden",
                    "Customer-primary_address_and_contact_detail-hidden",
                    "Customer-customer_primary_contact-hidden",
                    "Customer-mobile_no-hidden",
                    "Customer-email_id-hidden",
                    "Customer-column_break_26-hidden",
                    "Customer-customer_primary_address-hidden",
                    "Customer-primary_address-hidden"
                ]
            ]
        ]
    }
]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/vet_care/css/vet_care.css"
app_include_js = "/assets/js/vet_care.min.js"

# include js, css files in header of web template
# web_include_css = "/assets/vet_care/css/vet_care.css"
# web_include_js = "/assets/vet_care/js/vet_care.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Sales Invoice": "public/js/sales_invoice.js",
    "Inpatient Record": "public/js/inpatient_record.js",
    "Patient": "public/js/patient.js",
    "Vital Signs": "public/js/vital_signs.js",
    "Lab Test": "public/js/lab_test.js",
    "Patient Encounter": "public/js/patient_encounter.js",
    "Patient Appointment": "public/js/patient_appointment.js",
    "Customer": "public/js/customer.js",
    "Healthcare Practitioner": "public/js/healthcare_practitioner.js"
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "vet_care.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "vet_care.install.before_install"
# after_install = "vet_care.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "vet_care.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Patient": {
        "validate": "vet_care.doc_events.patient.validate",
        "before_save": "vet_care.doc_events.patient.before_save",
    },
    "Patient Appointment": {
        "validate": "vet_care.doc_events.patient_appointment.validate"
    },
    "Sales Invoice": {
        "validate": "vet_care.doc_events.sales_invoice.validate"
    },
    "Contact": {
        "validate": "vet_care.doc_events.contact.validate"
    },
    "Customer": {
        "validate": "vet_care.doc_events.customer.validate",
        "before_save": "vet_care.doc_events.customer.before_save",
        "on_update": "vet_care.doc_events.customer.on_update",
    },
    "Vital Signs": {
        "validate": "vet_care.doc_events.vital_signs.validate",
        "on_submit": "vet_care.doc_events.vital_signs.on_submit"
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"vet_care.tasks.all"
# 	],
# 	"daily": [
# 		"vet_care.tasks.daily"
# 	],
# 	"hourly": [
# 		"vet_care.tasks.hourly"
# 	],
# 	"weekly": [
# 		"vet_care.tasks.weekly"
# 	]
# 	"monthly": [
# 		"vet_care.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "vet_care.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
    "frappe.utils.print_format.download_pdf": "vet_care.whitelist_methods.print_format.download_pdf",
    "erpnext.healthcare.doctype.patient_appointment.patient_appointment.get_events": "vet_care.whitelist_methods.patient_appointment.get_events"
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "vet_care.task.get_dashboard_data"
# }
