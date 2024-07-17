frappe.ui.form.on('IMS User', {
    refresh(frm) {
        // If the password field is empty, generate a random password
        if (!frm.doc.password) {
            frm.set_value('password', frappe.utils.get_random(16));
        }
    },
    before_save(frm) {
        // If the password field is empty, generate a random password
        if (!frm.doc.password) {
            frm.set_value('password', frappe.utils.get_random(16));
        }
    }
});
