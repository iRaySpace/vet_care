import utils from './utils';

frappe.provide('vet_care');

vet_care = { utils };

frappe.ui.form.CustomerQuickEntryForm = frappe.ui.form.QuickEntryForm.extend({
    init: function(doctype, after_insert) {
		this._super(doctype, after_insert);
	},

	render_dialog: function() {
		this.mandatory = this.mandatory.concat(this.get_variant_fields());
		this._super();
	},

	get_variant_fields: function() {
		const variant_fields = [{
			fieldtype: "Section Break",
			label: __("Contact Details")
		},
		{
			label: __("CPR Number"),
			fieldname: "vc_cpr",
			fieldtype: "Data"
		},
		{
			label: __("Email Info"),
			fieldname: "email_info",
			fieldtype: "Data"
		},
		{
			label: __("Tax Id"),
			fieldname: "tax_id",
			fieldtype: "Data"
		},
		{
			fieldtype: "Column Break",
		},
		{
			label: __("Mobile Number"),
			fieldname: "mobile_number",
			fieldtype: "Data"
		},
		{
			label: __("Mobile Number 2"),
			fieldname: "mobile_number_2",
			fieldtype: "Data"
		},
		{
			label: __("Home Phone"),
			fieldname: "vc_home_phone",
			fieldtype: "Data"
		},
		{
			label: __("Office Phone"),
			fieldname: "vc_office_phone",
			fieldtype: "Data"
		}];
		return variant_fields;
	},
});
