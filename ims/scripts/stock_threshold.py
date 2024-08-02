import json
import os

from frappe import (
    _,
    get_doc,
    get_list,
    log_error,
    sendmail,
)
from frappe.utils import get_url
from jinja2 import Template


def after_save(doc, method=None):
    if get_doc("Stock Entry", doc.as_dict().voucher_no).as_dict().from_warehouse != doc.warehouse:
        return

    item_data = json.loads(get_doc("Item", doc.item_code).as_json())["stock_threshold"]

    bin_items = get_list(
        "Bin",
        fields=["name", "warehouse", "actual_qty", "item_code"],
        filters=[
            [
                "warehouse",
                "in",
                [d["warehouse"] for d in item_data],
            ],
            ["item_code", "in", [d["parent"] for d in item_data]],
        ],
    )
    try:
        filtered = list(
            map(
                lambda x, y: {**x, "stock_threshold": y},
                bin_items,
                [x["stock_threshold"] for x in item_data],
            )
        )

        data = list(filter(lambda x: x["actual_qty"] < x["stock_threshold"], filtered))
        print(data)

        current_dir = os.path.dirname(__file__)
        template_path = os.path.join(
            current_dir,
            "../inventory_management_system/email_templates/low_in_stock.html",
        )
        send_email(data, template_path)
    except Exception as e:
        print("err", e)
        log_error(f"Error sending email: {str(e)}", "Send Email Error")


def send_email(docs, template_path):
    try:
        with open(template_path) as file:
            html_content = file.read()
        template = Template(html_content)
        users = get_list(
            "User",
            fields=["email"],
            filters={"role": "Inventory Manager"},
            pluck="email",
        )
        print(docs)
        message = template.render(
            docs=docs,
            site_url=get_url(),
        )

        sendmail(recipients=users, subject=_("Low Stock Alert"), message=message)
    except Exception as e:
        log_error(f"Error sending email: {str(e)}", "Send Email Error")