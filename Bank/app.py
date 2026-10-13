"""
Simple Banking System — Flask Web Application
Preserves the original banking logic with a professional web frontend.
"""

import random
import hashlib
import secrets
from datetime import datetime
from flask import (
    Flask, render_template, request, redirect,
    url_for, session, jsonify, flash
)

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# ─── In-memory data store (seeded with 2 demo accounts for immediate testing) ───
accounts = {
    100001: {
        "name": "Alexander Wright",
        "phone": "9876543210",
        "pin": hashlib.sha256("1234".encode()).hexdigest(),
        "balance": 25000.0,
        "transactions": [
            {
                "type": "credit",
                "description": "Initial Opening Deposit",
                "amount": 25000.0,
                "balance_after": 25000.0,
                "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        ],
        "created_at": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
    },
    100002: {
        "name": "Sophia Vance",
        "phone": "9876543211",
        "pin": hashlib.sha256("1234".encode()).hexdigest(),
        "balance": 12500.0,
        "transactions": [
            {
                "type": "credit",
                "description": "Initial Opening Deposit",
                "amount": 12500.0,
                "balance_after": 12500.0,
                "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        ],
        "created_at": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
    },
}


def current_time():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


def hash_pin(pin: str) -> str:
    """Hash the PIN so we never store it in plain text."""
    return hashlib.sha256(pin.encode()).hexdigest()


def generate_account_number() -> int:
    number = random.randint(100000, 999999)
    while number in accounts:
        number = random.randint(100000, 999999)
    return number


# ─── Helper: get the currently logged-in account ───
def get_logged_in_account():
    acc_num = session.get("account_number")
    if acc_num is None:
        return None, None
    account = accounts.get(acc_num)
    if account is None:
        session.clear()
        return None, None
    return acc_num, account


# ────────────────────────────────────────────
#  PAGE ROUTES (serve HTML templates)
# ────────────────────────────────────────────

@app.route("/")
def index():
    acc_num, _ = get_logged_in_account()
    if acc_num:
        return redirect(url_for("dashboard"))
    return render_template("index.html")


@app.route("/register")
def register_page():
    return render_template("register.html")


@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    acc_num, account = get_logged_in_account()
    if acc_num is None:
        return redirect(url_for("login_page"))
    return render_template(
        "dashboard.html",
        account=account,
        account_number=acc_num,
    )


@app.route("/transactions")
def transactions_page():
    acc_num, account = get_logged_in_account()
    if acc_num is None:
        return redirect(url_for("login_page"))
    return render_template(
        "transactions.html",
        account=account,
        account_number=acc_num,
    )


@app.route("/transfer")
def transfer_page():
    acc_num, account = get_logged_in_account()
    if acc_num is None:
        return redirect(url_for("login_page"))
    return render_template(
        "transfer.html",
        account=account,
        account_number=acc_num,
    )


@app.route("/settings")
def settings_page():
    acc_num, account = get_logged_in_account()
    if acc_num is None:
        return redirect(url_for("login_page"))
    return render_template(
        "settings.html",
        account=account,
        account_number=acc_num,
    )


# ────────────────────────────────────────────
#  API ROUTES (JSON endpoints)
# ────────────────────────────────────────────

@app.route("/api/register", methods=["POST"])
def api_register():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    phone = (data.get("phone") or "").strip()
    pin = (data.get("pin") or "").strip()

    if not name or not phone:
        return jsonify({"success": False, "message": "Name and phone number are required."}), 400

    if len(pin) != 4 or not pin.isdigit():
        return jsonify({"success": False, "message": "PIN must be exactly 4 digits."}), 400

    if not phone.isdigit() or len(phone) < 10:
        return jsonify({"success": False, "message": "Enter a valid phone number (at least 10 digits)."}), 400

    account_number = generate_account_number()
    accounts[account_number] = {
        "name": name,
        "phone": phone,
        "pin": hash_pin(pin),
        "balance": 0.0,
        "transactions": [],
        "created_at": current_time(),
    }

    return jsonify({
        "success": True,
        "message": "Account created successfully.",
        "account_number": account_number,
    })


@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json(silent=True) or {}
    acc_text = (data.get("account_number") or "").strip()
    pin = (data.get("pin") or "").strip()

    if not acc_text.isdigit():
        return jsonify({"success": False, "message": "Invalid account number."}), 400

    acc_num = int(acc_text)
    account = accounts.get(acc_num)

    if account is None or account["pin"] != hash_pin(pin):
        return jsonify({"success": False, "message": "Incorrect account number or PIN."}), 401

    session["account_number"] = acc_num
    return jsonify({
        "success": True,
        "message": f"Welcome, {account['name']}!",
        "name": account["name"],
    })


@app.route("/api/logout", methods=["POST"])
def api_logout():
    session.clear()
    return jsonify({"success": True, "message": "Logged out successfully."})


@app.route("/api/balance", methods=["GET"])
def api_balance():
    acc_num, account = get_logged_in_account()
    if acc_num is None:
        return jsonify({"success": False, "message": "Not logged in."}), 401
    return jsonify({
        "success": True,
        "balance": account["balance"],
        "name": account["name"],
        "account_number": acc_num,
        "phone": account["phone"],
        "created_at": account.get("created_at", "N/A"),
    })


@app.route("/api/deposit", methods=["POST"])
def api_deposit():
    acc_num, account = get_logged_in_account()
    if acc_num is None:
        return jsonify({"success": False, "message": "Not logged in."}), 401

    data = request.get_json(silent=True) or {}
    try:
        amount = float(data.get("amount", 0))
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Enter a valid amount."}), 400

    if amount <= 0:
        return jsonify({"success": False, "message": "Amount must be greater than zero."}), 400

    account["balance"] += amount
    account["transactions"].insert(0, {
        "type": "credit",
        "description": f"Deposited Rs. {amount:,.2f}",
        "amount": amount,
        "balance_after": account["balance"],
        "time": current_time(),
    })

    return jsonify({
        "success": True,
        "message": f"Rs. {amount:,.2f} deposited successfully.",
        "balance": account["balance"],
    })


@app.route("/api/withdraw", methods=["POST"])
def api_withdraw():
    acc_num, account = get_logged_in_account()
    if acc_num is None:
        return jsonify({"success": False, "message": "Not logged in."}), 401

    data = request.get_json(silent=True) or {}
    try:
        amount = float(data.get("amount", 0))
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Enter a valid amount."}), 400

    if amount <= 0:
        return jsonify({"success": False, "message": "Amount must be greater than zero."}), 400

    if amount > account["balance"]:
        return jsonify({"success": False, "message": "Insufficient balance."}), 400

    account["balance"] -= amount
    account["transactions"].insert(0, {
        "type": "debit",
        "description": f"Withdrew Rs. {amount:,.2f}",
        "amount": amount,
        "balance_after": account["balance"],
        "time": current_time(),
    })

    return jsonify({
        "success": True,
        "message": f"Rs. {amount:,.2f} withdrawn successfully.",
        "balance": account["balance"],
    })


@app.route("/api/transfer", methods=["POST"])
def api_transfer():
    acc_num, account = get_logged_in_account()
    if acc_num is None:
        return jsonify({"success": False, "message": "Not logged in."}), 401

    data = request.get_json(silent=True) or {}
    receiver_text = (data.get("receiver") or "").strip()
    try:
        amount = float(data.get("amount", 0))
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Enter a valid amount."}), 400

    if not receiver_text.isdigit():
        return jsonify({"success": False, "message": "Invalid receiver account number."}), 400

    receiver_number = int(receiver_text)
    receiver = accounts.get(receiver_number)

    if receiver is None:
        return jsonify({"success": False, "message": "Receiver account not found."}), 404

    if receiver_number == acc_num:
        return jsonify({"success": False, "message": "Cannot transfer to your own account."}), 400

    if amount <= 0:
        return jsonify({"success": False, "message": "Amount must be greater than zero."}), 400

    if amount > account["balance"]:
        return jsonify({"success": False, "message": "Insufficient balance."}), 400

    account["balance"] -= amount
    receiver["balance"] += amount
    time_now = current_time()

    account["transactions"].insert(0, {
        "type": "debit",
        "description": f"Transferred Rs. {amount:,.2f} to A/C {receiver_number}",
        "amount": amount,
        "balance_after": account["balance"],
        "time": time_now,
    })
    receiver["transactions"].insert(0, {
        "type": "credit",
        "description": f"Received Rs. {amount:,.2f} from A/C {acc_num}",
        "amount": amount,
        "balance_after": receiver["balance"],
        "time": time_now,
    })

    return jsonify({
        "success": True,
        "message": f"Rs. {amount:,.2f} transferred to A/C {receiver_number}.",
        "balance": account["balance"],
    })


@app.route("/api/transactions", methods=["GET"])
def api_transactions():
    acc_num, account = get_logged_in_account()
    if acc_num is None:
        return jsonify({"success": False, "message": "Not logged in."}), 401
    return jsonify({
        "success": True,
        "transactions": account["transactions"],
    })


@app.route("/api/change-pin", methods=["POST"])
def api_change_pin():
    acc_num, account = get_logged_in_account()
    if acc_num is None:
        return jsonify({"success": False, "message": "Not logged in."}), 401

    data = request.get_json(silent=True) or {}
    old_pin = (data.get("old_pin") or "").strip()
    new_pin = (data.get("new_pin") or "").strip()
    confirm_pin = (data.get("confirm_pin") or "").strip()

    if hash_pin(old_pin) != account["pin"]:
        return jsonify({"success": False, "message": "Current PIN is incorrect."}), 401

    if len(new_pin) != 4 or not new_pin.isdigit():
        return jsonify({"success": False, "message": "New PIN must be exactly 4 digits."}), 400

    if new_pin != confirm_pin:
        return jsonify({"success": False, "message": "New PIN confirmation does not match."}), 400

    if old_pin == new_pin:
        return jsonify({"success": False, "message": "New PIN must be different from current PIN."}), 400

    account["pin"] = hash_pin(new_pin)
    return jsonify({"success": True, "message": "PIN changed successfully."})


# ────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=5000)
