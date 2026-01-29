import streamlit as st
import json
from bank import Bank
from account import Account
from transaction import Transaction

# Initialize Bank with JSON data
bank = Bank()

st.set_page_config(page_title="Bank Management System", layout="wide")
st.title("🏦 Bank Management System")

# Initialize session state
if 'current_account' not in st.session_state:
    st.session_state.current_account = None

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select an option", [
    "Dashboard",
    "Create Account",
    "View Accounts",
    "Account Operations",
    "Transaction History",
    "Delete Account"
])

# ==================== DASHBOARD ====================
if page == "Dashboard":
    st.header("📊 Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Accounts", len(Bank.accounts))
    
    with col2:
        st.metric("Total Transactions", len(Bank.transactions))
    
    st.subheader("Quick Stats")
    if Bank.accounts:
        total_balance = sum(float(acc.get('balance', 0)) for acc in Bank.accounts.values())
        st.metric("Total Balance Across All Accounts", f"${total_balance:.2f}")
    else:
        st.info("No accounts created yet.")

# ==================== CREATE ACCOUNT ====================
elif page == "Create Account":
    st.header("➕ Create New Account")
    
    with st.form("create_account_form"):
        name = st.text_input("Account Holder Name")
        account_type = st.selectbox("Account Type", ["Savings", "Current", "Checking"])
        initial_balance = st.number_input("Initial Balance", min_value=0.0, step=100.0)
        
        submitted = st.form_submit_button("Create Account")
        
        if submitted:
            if name.strip() == "":
                st.error("❌ Name cannot be empty")
            else:
                try:
                    acc_num = Bank.create_account(name, account_type.lower(), initial_balance)
                    st.success(f"✅ Account created successfully!")
                    st.info(f"Account Number: **{acc_num}**\nName: **{name}**\nType: **{account_type}**\nBalance: **${initial_balance}**")
                except Exception as e:
                    st.error(f"❌ Error creating account: {e}")

# ==================== VIEW ACCOUNTS ====================
elif page == "View Accounts":
    st.header("👥 View All Accounts")
    
    if not Bank.accounts:
        st.warning("No accounts found in the system.")
    else:
        # Display accounts in a nice format
        col_headers = st.columns(4)
        with col_headers[0]:
            st.subheader("Account #")
        with col_headers[1]:
            st.subheader("Holder Name")
        with col_headers[2]:
            st.subheader("Type")
        with col_headers[3]:
            st.subheader("Balance")
        
        st.divider()
        
        for acc_num, details in Bank.accounts.items():
            cols = st.columns(4)
            with cols[0]:
                st.write(acc_num)
            with cols[1]:
                st.write(details.get('name', 'N/A'))
            with cols[2]:
                st.write(details.get('account_type', 'N/A').capitalize())
            with cols[3]:
                st.write(f"${details.get('balance', 0):.2f}")
            
            st.divider()

# ==================== ACCOUNT OPERATIONS ====================
elif page == "Account Operations":
    st.header("💰 Account Operations")
    
    if not Bank.accounts:
        st.warning("No accounts available. Create an account first.")
    else:
        # Select account
        account_options = {f"{num} - {details['name']}": num for num, details in Bank.accounts.items()}
        selected_account = st.selectbox("Select Account", list(account_options.keys()))
        acc_num = account_options[selected_account]
        
        # Load account
        try:
            customer = Account(acc_num)
            
            # Display current balance
            st.info(f"**Current Balance: ${customer.get_balance:.2f}**")
            
            st.divider()
            
            # Operation tabs
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("💸 Deposit")
                deposit_amount = st.number_input("Deposit Amount", min_value=0.0, step=50.0, key="deposit")
                if st.button("Deposit Now", key="deposit_btn"):
                    if deposit_amount > 0:
                        try:
                            customer.deposit(deposit_amount)
                            st.success(f"✅ Deposited ${deposit_amount:.2f} successfully!")
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
                    else:
                        st.error("❌ Please enter a valid amount")
            
            with col2:
                st.subheader("🏧 Withdraw")
                withdraw_amount = st.number_input("Withdrawal Amount", min_value=0.0, step=50.0, key="withdraw")
                if st.button("Withdraw Now", key="withdraw_btn"):
                    if withdraw_amount > 0:
                        if withdraw_amount <= customer.get_balance:
                            try:
                                customer.withdraw(withdraw_amount)
                                st.success(f"✅ Withdrawn ${withdraw_amount:.2f} successfully!")
                            except Exception as e:
                                st.error(f"❌ Error: {e}")
                        else:
                            st.error(f"❌ Insufficient balance! Available: ${customer.get_balance:.2f}")
                    else:
                        st.error("❌ Please enter a valid amount")
            
            st.divider()
            
            # Display account details
            st.subheader("📋 Account Details")
            details_col1, details_col2 = st.columns(2)
            with details_col1:
                st.metric("Account Number", acc_num)
                st.metric("Holder Name", customer.holder_name)
            with details_col2:
                st.metric("Account Type", customer.acc_type.capitalize())
                st.metric("Current Balance", f"${customer.get_balance:.2f}")
                
        except ValueError as e:
            st.error(f"❌ {e}")
        except Exception as e:
            st.error(f"❌ Error loading account: {e}")

# ==================== TRANSACTION HISTORY ====================
elif page == "Transaction History":
    st.header("📝 Transaction History")
    
    if not Bank.accounts:
        st.warning("No accounts available.")
    else:
        # Select account
        account_options = {f"{num} - {details['name']}": num for num, details in Bank.accounts.items()}
        selected_account = st.selectbox("Select Account", list(account_options.keys()), key="trans_select")
        acc_num = account_options[selected_account]
        
        # Filter transactions for selected account
        account_transactions = [t for t in Bank.transactions if str(t['account_num']) == str(acc_num)]
        
        if not account_transactions:
            st.info("No transactions yet for this account.")
        else:
            st.subheader(f"Transactions for Account {acc_num}")
            
            # Display transactions
            for trans in account_transactions:
                with st.container(border=True):
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.write(f"**Trans ID:** {trans['trans_id']}")
                    with col2:
                        trans_type = trans['trans_type'].capitalize()
                        if trans['trans_type'] == 'deposit':
                            st.write(f"✅ **{trans_type}**")
                        else:
                            st.write(f"🔄 **{trans_type}**")
                    with col3:
                        st.write(f"**Amount:** ${trans['amount']:.2f}")
                    with col4:
                        st.write(f"**Time:** {trans['time']}")

# ==================== DELETE ACCOUNT ====================
elif page == "Delete Account":
    st.header("🗑️ Delete Account")
    
    st.warning("⚠️ Warning: This action cannot be undone!")
    
    if not Bank.accounts:
        st.warning("No accounts available to delete.")
    else:
        # Select account to delete
        account_options = {f"{num} - {details['name']}": num for num, details in Bank.accounts.items()}
        selected_account = st.selectbox("Select Account to Delete", list(account_options.keys()), key="delete_select")
        acc_num = account_options[selected_account]
        
        # Get account details
        acc_details = Bank.accounts.get(acc_num)
        if acc_details:
            st.info(f"**Account to Delete:**\n- Number: {acc_num}\n- Name: {acc_details['name']}\n- Balance: ${acc_details['balance']:.2f}")
        
        # Confirmation
        st.write("Type the account number to confirm deletion:")
        confirmation = st.text_input("Confirm by entering account number", key="delete_confirm")
        
        if st.button("Delete Account", type="secondary"):
            if confirmation == str(acc_num):
                try:
                    bank.delete_account(acc_num)
                    st.success(f"✅ Account {acc_num} deleted successfully!")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Error deleting account: {e}")
            else:
                st.error("❌ Account number does not match. Deletion cancelled.")

# Footer
st.divider()
st.markdown("---")
st.markdown("💼 Bank Management System | Powered by Streamlit")
