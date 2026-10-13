# SecureBank — Digital Retail Banking System

A full-stack, enterprise-grade banking application built on **Python Flask** and **Vanilla HTML/CSS/JS**. It expands the core banking system with an authentic, institutional web interface without altering the underlying banking rules.

---

## 🏛️ System Capabilities & Architecture

- **Account Lifecycle:**
  - Fast onboarding with name, phone, and 4-digit PIN.
  - Automatic generation of unique 6-digit Account Numbers.
  - SHA-256 cryptographic hashing for PIN security (no plain text storage).

- **Financial Ledger & Operations:**
  - Real-time balance enquiry with privacy mask toggle (`₹ ••••••••`).
  - Cash Deposit with instant ledger credit.
  - Cash Withdrawal with balance validation and overdraft protection.
  - Direct Intra-Bank Transfer between account holders with self-transfer prevention and immediate counter-party balance updates.
  - Itemized Statement with chronologically ordered credit/debit badges, running balance tracking, filter tabs (Credits / Debits), and printable statement layout.

- **Security Administration:**
  - Secure NetBanking authentication.
  - In-session PIN update requiring validation against current PIN.
  - Session management and one-click secure termination.

---

## 🚀 How to Run the Banking Web App

1. Ensure Flask is installed:
   ```bash
   pip install flask
   ```

2. Start the web server:
   ```bash
   python app.py
   ```

3. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

---

## 🧪 Pre-Seeded Demo Accounts for Immediate Testing

You can register a new account immediately, or sign in using any of the pre-configured demo test accounts:

| Account Holder | Account Number | Security PIN | Initial Balance |
| :--- | :---: | :---: | :---: |
| **Alexander Wright** | `100001` | `1234` | ₹25,000.00 |
| **Sophia Vance** | `100002` | `1234` | ₹12,500.00 |

*(You can transfer funds back and forth between Account 100001 and 100002 to test real-time settlement!)*

---

## 📁 Project Structure

```
Bank/
├── app.py                  # Flask backend with secure REST APIs & web routes
├── banking_system.py       # Original command-line interface script
├── static/
│   ├── css/
│   │   └── style.css       # Institutional dark banking UI design system
│   └── js/
│       └── app.js          # Modal management, toast alerts, API requests
└── templates/
    ├── base.html           # Authenticated layout with sidebar & mobile menu
    ├── index.html          # Gateway welcome page
    ├── login.html          # NetBanking sign-in with demo autofill
    ├── register.html       # New account onboarding & ID generation modal
    ├── dashboard.html      # Account overview, live balance, quick actions
    ├── transactions.html   # Statement ledger with search & credit/debit filters
    ├── transfer.html       # Inter-account funds transfer interface
    └── settings.html       # Security PIN modification & profile standing
```
