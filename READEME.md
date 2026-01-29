# Bank Management System - Streamlit Frontend

## Features

- **Dashboard**: Overview of total accounts, transactions, and balances
- **Create Account**: Create new bank accounts with initial balance
- **View Accounts**: Display all accounts with details
- **Account Operations**: 
  - Deposit money
  - Withdraw money
  - View current balance
- **Transaction History**: View all transactions for each account
- **Delete Account**: Remove accounts with confirmation

## Installation

1. Install Streamlit:
```bash
pip install -r requirements.txt
```

Or install directly:
```bash
pip install streamlit
```

## Running the App

Navigate to the project directory and run:

```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

## Project Structure

```
Bank-Management-system/
├── bank.py              # Bank class with account management
├── account.py           # Account class with operations (deposit/withdraw)
├── transaction.py       # Transaction tracking
├── streamlit_app.py     # Streamlit frontend
├── record.json          # Account data storage
└── requirements.txt     # Dependencies
```

## Backend Classes

- **Bank**: Core banking operations (create/delete accounts, list accounts)
- **Account**: Individual account operations (deposit, withdraw, get details)
- **Transaction**: Transaction tracking and history

## Usage

1. **Create Account**: Go to "Create Account" section, enter holder name, type, and initial balance
2. **Perform Operations**: Select an account and deposit/withdraw money
3. **View History**: Check transaction history for any account
4. **Manage Accounts**: View all accounts or delete specific accounts

---
All data is persisted in `record.json`
