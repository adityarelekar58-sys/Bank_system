import random
from datetime import datetime


accounts = {}


def current_time():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


def create_account():
    print("\n--- Create Account ---")
    name = input("Enter your name: ").strip()
    phone = input("Enter your phone number: ").strip()
    pin = input("Create a 4-digit PIN: ").strip()

    if not name or not phone:
        print("Name and phone number cannot be empty.")
        return

    if len(pin) != 4 or not pin.isdigit():
        print("PIN must contain exactly 4 digits.")
        return

    account_number = random.randint(100000, 999999)
    while account_number in accounts:
        account_number = random.randint(100000, 999999)

    accounts[account_number] = {
        "name": name,
        "phone": phone,
        "pin": pin,
        "balance": 0.0,
        "transactions": []
    }

    print("Account created successfully.")
    print("Your account number is:", account_number)


def login():
    print("\n--- Login ---")
    account_text = input("Enter account number: ").strip()
    pin = input("Enter PIN: ").strip()

    if not account_text.isdigit():
        print("Invalid account number.")
        return None

    account_number = int(account_text)
    account = accounts.get(account_number)

    if account is None or account["pin"] != pin:
        print("Incorrect account number or PIN.")
        return None

    print("Login successful. Welcome,", account["name"] + "!")
    return account_number


def check_balance(account):
    print(f"Current balance: Rs. {account['balance']:.2f}")


def deposit(account):
    print("\n--- Deposit Money ---")
    amount_text = input("Enter amount to deposit: ").strip()

    try:
        amount = float(amount_text)
    except ValueError:
        print("Please enter a valid amount.")
        return

    if amount <= 0:
        print("Amount must be greater than zero.")
        return

    account["balance"] += amount
    account["transactions"].append(
        f"{current_time()} - Deposited Rs. {amount:.2f}"
    )
    print("Money deposited successfully.")
    check_balance(account)


def withdraw(account):
    print("\n--- Withdraw Money ---")
    amount_text = input("Enter amount to withdraw: ").strip()

    try:
        amount = float(amount_text)
    except ValueError:
        print("Please enter a valid amount.")
        return

    if amount <= 0:
        print("Amount must be greater than zero.")
        return

    if amount > account["balance"]:
        print("Insufficient balance.")
        return

    account["balance"] -= amount
    account["transactions"].append(
        f"{current_time()} - Withdrew Rs. {amount:.2f}"
    )
    print("Please collect your money.")
    check_balance(account)


def transfer(account_number):
    account = accounts[account_number]
    print("\n--- Transfer Money ---")
    receiver_text = input("Enter receiver account number: ").strip()

    if not receiver_text.isdigit():
        print("Invalid account number.")
        return

    receiver_number = int(receiver_text)
    receiver = accounts.get(receiver_number)

    if receiver is None:
        print("Receiver account was not found.")
        return

    if receiver_number == account_number:
        print("You cannot transfer money to the same account.")
        return

    amount_text = input("Enter amount to transfer: ").strip()
    try:
        amount = float(amount_text)
    except ValueError:
        print("Please enter a valid amount.")
        return

    if amount <= 0:
        print("Amount must be greater than zero.")
        return

    if amount > account["balance"]:
        print("Insufficient balance.")
        return

    account["balance"] -= amount
    receiver["balance"] += amount
    time = current_time()

    account["transactions"].append(
        f"{time} - Transferred Rs. {amount:.2f} to account {receiver_number}"
    )
    receiver["transactions"].append(
        f"{time} - Received Rs. {amount:.2f} from account {account_number}"
    )

    print("Money transferred successfully.")
    check_balance(account)


def show_history(account):
    print("\n--- Transaction History ---")
    if not account["transactions"]:
        print("No transactions yet.")
        return

    for number, transaction in enumerate(account["transactions"], start=1):
        print(f"{number}. {transaction}")


def change_pin(account):
    print("\n--- Change PIN ---")
    old_pin = input("Enter old PIN: ").strip()

    if old_pin != account["pin"]:
        print("Old PIN is incorrect.")
        return

    new_pin = input("Enter new 4-digit PIN: ").strip()
    confirm_pin = input("Confirm new PIN: ").strip()

    if len(new_pin) != 4 or not new_pin.isdigit():
        print("PIN must contain exactly 4 digits.")
        return

    if new_pin != confirm_pin:
        print("PIN confirmation does not match.")
        return

    account["pin"] = new_pin
    print("PIN changed successfully.")


def account_menu(account_number):
    account = accounts[account_number]

    while True:
        print("\n--- Account Menu ---")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Transaction History")
        print("6. Change PIN")
        print("7. Logout")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            check_balance(account)
            input("Press Enter to return to the account menu...")
        elif choice == "2":
            deposit(account)
        elif choice == "3":
            withdraw(account)
        elif choice == "4":
            transfer(account_number)
        elif choice == "5":
            show_history(account)
            input("Press Enter to return to the account menu...")
        elif choice == "6":
            change_pin(account)
        elif choice == "7":
            print("Logged out successfully.")
            break
        else:
            print("Invalid choice. Please try again.")


def main():
    while True:
        print("\n===== Simple Banking System (CLI Mode) =====")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            create_account()
        elif choice == "2":
            account_number = login()
            if account_number is not None:
                account_menu(account_number)
        elif choice == "3":
            print("Thank you for using the Banking System.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    import os
    import sys
    import webbrowser
    import threading

    # If --cli flag is passed, run terminal interface
    if "--cli" in sys.argv:
        main()
    else:
        print("\n" + "=" * 56)
        print("      SECUREBANK — ONLINE BANKING PORTAL")
        print("=" * 56)
        print("  Starting core banking server on http://127.0.0.1:5000")
        print("  Opening browser automatically...")
        print("  (Tip: Run with --cli to use terminal interface)")
        print("=" * 56 + "\n")

        try:
            import app

            # Open browser exactly once (avoiding duplicate tab from reloader)
            if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
                threading.Timer(1.2, lambda: webbrowser.open_new("http://127.0.0.1:5000")).start()

            app.app.run(debug=True, port=5000, use_reloader=False)
        except Exception as e:
            print(f"Could not start web server: {e}")
            print("Switching to terminal mode...")
            main()
