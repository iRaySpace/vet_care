// Copyright (c) 2016, 9T9IT and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Patient History"] = {
	"filters": [
        {
            fieldname: 'patient',
            label: __('Patient'),
            fieldtype: 'Link',
            options: 'Patient',
            on_change: function(report) {
                _set_patient_information(report);
                report.refresh();
            }
        },

        // metadata for html print
        {
            fieldname: 'patient_name',
            fieldtype: 'Data',
            hidden: true,
        },
        {
            fieldname: 'customer_name',
            fieldtype: 'Data',
            hidden: true,
        },
        {
            fieldname: 'patient_dob',
            fieldtype: 'Date',
            hidden: true,
        },
        {
            fieldname: 'species',
            fieldtype: 'Data',
            hidden: true,
        },
        {
            fieldname: 'breed',
            fieldtype: 'Data',
            hidden: true,
        },
        {
            fieldname: 'color',
            fieldtype: 'Data',
            hidden: true,
        },
        {
            fieldname: 'chip_id',
            fieldtype: 'Data',
            hidden: true,
        },
        {
            fieldname: 'neutered',
            fieldtype: 'Data',
            hidden: true,
        },
        {
            fieldname: 'deceased',
            fieldtype: 'Data',
            hidden: true
        },
        {
            fieldname: 'posting_date',
            fieldtype: 'Date',
            hidden: true,
            default: frappe.datetime.get_today(),
        }
	]
};

async function _set_patient_information(report) {
    const patient_information = await frappe.db.get_doc('Patient', report.get_filter_value('patient'));
    const customer_name = await frappe.db.get_value('Customer', patient_information.customer, 'customer_name');
    const mapped_fields = {
        'patient_name': patient_information.patient_name,
        'customer_name': customer_name,
        'patient_dob': patient_information.dob,
        'color': patient_information.vc_color,
        'species': patient_information.vc_species,
        'breed': patient_information.vc_breed,
        'chip_id': patient_information.vc_chip_id,
        'neutered': patient_information.vc_neutered,
        'deceased': patient_information.vc_deceased ? 'Yes' : 'No'
    };
    Object.keys(mapped_fields).forEach((key) =>
        report.set_filter_value(key, mapped_fields[key])
    );
}
