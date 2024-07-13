import frappe

def delete_communication_if_email_sent(doc, method):
    if doc.doctype == 'Email Queue' and doc.reference_doctype == 'IMS User' and doc.status == 'Sent':
        communication_id = doc.communication
        if communication_id:
            frappe.delete_doc('Communication', communication_id)
            frappe.db.commit()