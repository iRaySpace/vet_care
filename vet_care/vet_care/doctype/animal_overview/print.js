function print_history(frm) {
  frappe.ui.get_print_settings(
      false,
      print_settings => _print({
        patient: frm.doc.animal,
        data: frm.clinical_history,
      }, print_settings),
      null,
  );
}


// https://github.com/frappe/frappe/blob/version-11/frappe/public/js/frappe/views/reports/query_report.js#L823
function _print(data, print_settings) {
  const base_url = frappe.urllib.get_base_url();
  const print_css = frappe.boot.print_css;
  const landscape = print_settings.orientation == 'Landscape';
  const content = frappe.render_template('clinical_history', {
    patient: data.patient,
    data: data.data,
  });
  const html = frappe.render_template('print_template', {
      title: 'Clinical History',
      columns: [],
      content,
      base_url,
      print_css,
      print_settings,
      landscape,
  });
  frappe.render_pdf(html, print_settings);
}
