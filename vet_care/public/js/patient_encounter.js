frappe.ui.form.on('Patient Encounter', {
  refresh: function(frm) {
    if (frm.doc.docstatus) {
      _make_invoice_btn(frm);
    }
  }
});

function _make_invoice_btn(frm) {
  frm.add_custom_button('Make Invoice', async () => {
    const { message: invoice } = await frappe.call({
      method: 'vet_care.api.make_invoice_for_encounter',
      args: { 'dt': frm.doc.doctype, 'dn': frm.doc.name },
    });
    const doclist = frappe.model.sync(invoice);
    frappe.set_route('Form', doclist[0].doctype, doclist[0].name);
  });
}
