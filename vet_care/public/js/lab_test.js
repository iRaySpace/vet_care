frappe.ui.form.on('Lab Test', {
  refresh: function(frm) {
    if (frm.doc.docstatus) {
      _make_invoivce_btn(frm);
    }
  },
});

function _make_invoivce_btn(frm) {
  frm.add_custom_button('Make Invoice', async () => {
    const { message: invoice } = await frappe.call({
      method: 'vet_care.api.make_invoice',
      args: { 'dt': 'Lab Test', 'dn': frm.doc.name },
    });
    const doclist = frappe.model.sync(invoice);
    frappe.set_route('Form', doclist[0].doctype, doclist[0].name);
  })
}