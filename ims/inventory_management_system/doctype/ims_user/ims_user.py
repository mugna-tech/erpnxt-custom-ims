import os

import frappe
from frappe import get_doc
from frappe.model.document import Document
from jinja2 import Template


class IMSUser(Document):
    def after_insert(self):
        create_user_and_send_email(self)


def create_user_and_send_email(doc):
    try:
        # Extend Functionality of the User Core DOCTYPE and add the fields from IMS User DOCTYPE
        user_doc = get_doc(
            {
                "doctype": "User",
                "first_name": doc.first_name,
                "email": doc.email,
                "send_welcome_email": 0,
                "new_password": doc.password,
                "roles": [{"role": doc.roles}],
            }
        )

        user_doc.flags.ignore_mandatory = True
        user_doc.run_method("onload")
        user_doc.run_method("set_missing_values")
        user_doc.insert()
        user_doc.save()
        frappe.msgprint(f"A user with email {doc.email} has been created")

        current_dir = os.path.dirname(__file__)
        template_path = os.path.join(current_dir, "../../email_templates/welcome_email.html")
        send_welcome_email(doc, template_path)
    except Exception as e:
        frappe.log_error(f"Error creating user: {str(e)}", "Create User Error")


def send_welcome_email(doc, template_path):
    try:
        with open(template_path) as file:
            html_content = file.read()
        template = Template(html_content)
        message = template.render(
            first_name=doc.first_name, email=doc.email, password=doc.password, roles=doc.roles
        )

        frappe.sendmail(recipients=doc.email, subject="Welcome to MUGNA IMS!", message=message)
    except Exception as e:
        frappe.log_error(f"Error sending welcome email: {str(e)}", "Send Welcome Email Error")
