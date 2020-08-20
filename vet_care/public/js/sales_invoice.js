frappe.ui.form.on('Sales Invoice', {
    onload: function(frm) {
        _get_show_zip_code().then((show_zip_code) => {
            // read only fields can't be set through set_df_property
            if (!show_zip_code) {
                $('div[title="vc_zip_code"]').hide();
            }
        });
    },
    refresh: function(frm) {
        _set_zip_code(frm);
    },
    patient: function(frm) {

    },
});


async function _set_zip_code(frm) {
    const { message: customer } = await frappe.db.get_value('Customer', frm.doc.customer, 'vc_zip_code');
    setTimeout(() => frm.fields_dict.vc_zip_code.set_input(customer.vc_zip_code), 150);
}


async function _get_show_zip_code() {
    const show_zip_code = await frappe.db.get_single_value('Vetcare Settings', 'show_zip_code');
    return show_zip_code;
}
