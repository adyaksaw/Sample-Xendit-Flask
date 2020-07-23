import os
import time

from xendit import Xendit, XenditError
import xendit
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/pay", methods=["POST"])
def pay():
    name = request.form.get("name")
    amount = request.form.get("amount")
    phone = request.form.get("phone_number")
    args = {
        "external_id": f"ovo-pay-{int(time.time())}",
        "amount": amount,
        "phone": phone,
    }
    xendit_instance = Xendit(api_key=os.getenv("XENDIT_API_KEY"))
    try:
        ovo_payment = xendit_instance.EWallet.create_ovo_payment(**args)
        return vars(ovo_payment)
    except XenditError as e:
        return vars(e)


@app.route("/webhook", methods=["POST"])
def catch_webhook():
    print(request.json)
    return {}

if __name__ == "__main__":
    app.run(debug=True)