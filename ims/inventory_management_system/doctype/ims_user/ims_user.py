import frappe
from frappe.model.document import Document
from frappe import get_doc

class IMSUser(Document):
    def after_insert(self):
        create_user_and_send_email(self)

def create_user_and_send_email(doc):
    try:
        #Extend Functionality of the User Core DOCTYPE and add the fields from IMS User DOCTYPE
        user_doc = get_doc({
            "doctype": "User",
            "first_name": doc.first_name,
            "email": doc.email,
            "send_welcome_email": 0,
            "new_password": doc.password,
            "roles": [{"role": doc.roles}]
        })

        user_doc.flags.ignore_mandatory = True
        user_doc.run_method("onload")
        user_doc.run_method("set_missing_values")
        user_doc.insert()
        user_doc.save()

        frappe.msgprint(f"A user with email {doc.email} has been created")

        # Send a welcome email to the new user
        send_welcome_email(doc)
    except Exception as e:
        frappe.log_error(f"Error creating user: {str(e)}", "Create User Error")

def send_welcome_email(doc):
    try:
        message = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; border: 1px solid #dcdcdc; border-radius: 5px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h2 style="text-align: center;">Welcome to MUGNA IMS!</h2>
                <p style="font-size: 16px; color: #333;">Dear {doc.first_name},</p>
                <p style="font-size: 16px; color: #333;">Welcome aboard!</p>
                <p style="font-size: 16px; color: #333;">You have successfully been registered as <strong>{doc.roles}</strong> on our platform.</p>
                <p style="font-size: 16px; color: #333;">You can access the site through this link: <a href="http://site1.local:8000/">http://site1.local:8000/</a></p>
                <p style="font-size: 16px; color: #333;">Your login details are:</p>
                <ul style="font-size: 16px; color: #333; list-style: none; padding: 0;">
                    <li><strong>Email:</strong> {doc.email}</li>
                    <li><strong>Password:</strong> {doc.password}</li>
                </ul>
                <p style="font-size: 16px; color: #333;">We're excited to have you join our community! Please use the above credentials to access your account.</p>
                <p style="font-size: 16px; color: #333;">Best regards,</p>
                <p style="font-size: 16px; color: #333;">MUGNA TECH - IMS</p>
            </div>
        """

        # Send the email using Frappe's sendmail function
        frappe.sendmail(
            recipients=doc.email,
            sender="denzkei12@gmail.com",
            subject="Welcome to MUGNA IMS!",
            message=message
        )
    except Exception as e:
        frappe.log_error(f"Error sending welcome email: {str(e)}", "Send Welcome Email Error")
        
