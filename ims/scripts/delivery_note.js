frappe.ui.form.on("Delivery Note", {
	is_return: function (frm) {
		frm.toggle_display(["custom_reason"], frm.doc.is_return);
	},
});
