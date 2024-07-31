frappe.ui.form.on("Sales Invoice", {
	is_return: function (frm) {
		frm.toggle_display(["custom_reason"], frm.doc.is_return);
	},
});
