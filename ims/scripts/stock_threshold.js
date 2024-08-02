frappe.ui.form.on("Stock Threshold", "item_stock", function (frm) {
	frappe.call({
		method: "frappe.client.get_list",
		args: {
			doctype: "Bin",
			item_code: frm.doc.item_code,
			warehouse: frm.doc.warehouse,
			fields: ["actual_qty"],
		},
		callback: function (r) {
			console.log(r);
		},
	});
	frappe.msgprint("ye");
});
