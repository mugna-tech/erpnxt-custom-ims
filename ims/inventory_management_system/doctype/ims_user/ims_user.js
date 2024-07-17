function generateRandomPassword(length) {
    let charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    let password = "";
    for (let i = 0; i < length; i++) {
        password += charset[Math.floor(Math.random() * charset.length)];
    }
    return password;
}

frappe.ui.form.on('IMS User', {
    refresh(frm) {
        // If the password field is empty, generate a random password
        if (!frm.doc.password) {
            frm.set_value('password', generateRandomPassword(12));
        }
    },
    before_save(frm) {
        // If the password field is empty, generate a random password
        if (!frm.doc.password) {
            frm.set_value('password', generateRandomPassword(12));
        }
    }
});
