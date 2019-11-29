frappe.ui.form.on('Vital Signs', {
    refresh: function(frm) {
        if (frm.doc.docstatus) {
            _make_encounter_btn(frm);
        }
    }
});

function _make_encounter_btn(frm) {
    frm.add_custom_button('Make Encounter', () => {
        frappe.route_options = {
            patient: frm.doc.patient,
            encounter_date: frm.doc.signs_date,
        };
        frappe.new_doc('Patient Encounter');
    });
}
