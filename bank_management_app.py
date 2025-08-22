import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import bcrypt
import json
import uuid
from datetime import datetime, timedelta
import random
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="SecureBank Pro",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI/UX
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .account-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }
    
    .transaction-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    
    .balance-display {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
        margin: 1rem 0;
    }
    
    .success-message {
        background: linear-gradient(90deg, #56ab2f 0%, #a8e6cf 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    
    .error-message {
        background: linear-gradient(90deg, #ff416c 0%, #ff4b2b 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

class BankDatabase:
    def __init__(self):
        self.db_path = "bank_system.db"
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Accounts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                account_number TEXT PRIMARY KEY,
                user_id INTEGER,
                account_type TEXT NOT NULL,
                balance REAL DEFAULT 0.0,
                account_holder_name TEXT NOT NULL,
                phone_number TEXT,
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'active',
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_number TEXT,
                transaction_type TEXT NOT NULL,
                amount REAL NOT NULL,
                balance_after REAL NOT NULL,
                description TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                reference_number TEXT UNIQUE,
                FOREIGN KEY (account_number) REFERENCES accounts (account_number)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def register_user(self, username, password, email):
        """Register a new user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute(
                "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
                (username, password_hash, email)
            )
            conn.commit()
            return True, "User registered successfully!"
        except sqlite3.IntegrityError:
            return False, "Username or email already exists!"
        finally:
            conn.close()
    
    def authenticate_user(self, username, password):
        """Authenticate user login"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()
        
        if result and bcrypt.checkpw(password.encode('utf-8'), result[1]):
            return True, result[0]
        return False, None
    
    def create_account(self, user_id, account_type, name, phone, address, initial_deposit=0):
        """Create a new bank account"""
        account_number = self.generate_account_number()
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO accounts 
                (account_number, user_id, account_type, balance, account_holder_name, phone_number, address)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (account_number, user_id, account_type, initial_deposit, name, phone, address))
            
            if initial_deposit > 0:
                self.add_transaction(account_number, "deposit", initial_deposit, initial_deposit, 
                                   "Initial deposit", cursor)
            
            conn.commit()
            return True, account_number
        except Exception as e:
            conn.rollback()
            return False, str(e)
        finally:
            conn.close()
    
    def generate_account_number(self):
        """Generate a unique account number"""
        return f"ACC{random.randint(100000000, 999999999)}"
    
    def get_user_accounts(self, user_id):
        """Get all accounts for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT account_number, account_type, balance, account_holder_name, 
                   phone_number, address, created_at, status
            FROM accounts WHERE user_id = ?
        ''', (user_id,))
        
        accounts = cursor.fetchall()
        conn.close()
        return accounts
    
    def get_account_details(self, account_number):
        """Get account details"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT account_number, account_type, balance, account_holder_name, 
                   phone_number, address, created_at, status
            FROM accounts WHERE account_number = ?
        ''', (account_number,))
        
        account = cursor.fetchone()
        conn.close()
        return account
    
    def update_balance(self, account_number, new_balance):
        """Update account balance"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE accounts SET balance = ? WHERE account_number = ?",
            (new_balance, account_number)
        )
        conn.commit()
        conn.close()
    
    def add_transaction(self, account_number, transaction_type, amount, balance_after, description, cursor=None):
        """Add a transaction record"""
        reference_number = f"TXN{uuid.uuid4().hex[:10].upper()}"
        
        if cursor:
            cursor.execute('''
                INSERT INTO transactions 
                (account_number, transaction_type, amount, balance_after, description, reference_number)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (account_number, transaction_type, amount, balance_after, description, reference_number))
        else:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO transactions 
                (account_number, transaction_type, amount, balance_after, description, reference_number)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (account_number, transaction_type, amount, balance_after, description, reference_number))
            conn.commit()
            conn.close()
        
        return reference_number
    
    def get_transactions(self, account_number, limit=50):
        """Get transaction history for an account"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT transaction_type, amount, balance_after, description, timestamp, reference_number
            FROM transactions 
            WHERE account_number = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (account_number, limit))
        
        transactions = cursor.fetchall()
        conn.close()
        return transactions
    
    def transfer_money(self, from_account, to_account, amount):
        """Transfer money between accounts"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Get source account details
            cursor.execute("SELECT balance FROM accounts WHERE account_number = ?", (from_account,))
            source_balance = cursor.fetchone()
            
            if not source_balance or source_balance[0] < amount:
                return False, "Insufficient balance or invalid source account"
            
            # Check if destination account exists
            cursor.execute("SELECT balance FROM accounts WHERE account_number = ?", (to_account,))
            dest_balance = cursor.fetchone()
            
            if not dest_balance:
                return False, "Destination account not found"
            
            # Perform the transfer
            new_source_balance = source_balance[0] - amount
            new_dest_balance = dest_balance[0] + amount
            
            cursor.execute("UPDATE accounts SET balance = ? WHERE account_number = ?", 
                         (new_source_balance, from_account))
            cursor.execute("UPDATE accounts SET balance = ? WHERE account_number = ?", 
                         (new_dest_balance, to_account))
            
            # Add transaction records
            ref_num = self.add_transaction(from_account, "transfer_out", amount, new_source_balance, 
                                         f"Transfer to {to_account}", cursor)
            self.add_transaction(to_account, "transfer_in", amount, new_dest_balance, 
                               f"Transfer from {from_account}", cursor)
            
            conn.commit()
            return True, f"Transfer successful! Reference: {ref_num}"
            
        except Exception as e:
            conn.rollback()
            return False, str(e)
        finally:
            conn.close()

# Initialize database
db = BankDatabase()

def main():
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'username' not in st.session_state:
        st.session_state.username = None

    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏦 SecureBank Pro</h1>
        <p>Your Modern Digital Banking Solution</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.authenticated:
        show_auth_page()
    else:
        show_banking_dashboard()

def show_auth_page():
    """Display authentication page"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
        
        with tab1:
            st.subheader("Welcome Back!")
            with st.form("login_form"):
                username = st.text_input("Username", placeholder="Enter your username")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                submit_login = st.form_submit_button("Login", use_container_width=True)
                
                if submit_login:
                    if username and password:
                        success, user_id = db.authenticate_user(username, password)
                        if success:
                            st.session_state.authenticated = True
                            st.session_state.user_id = user_id
                            st.session_state.username = username
                            st.rerun()
                        else:
                            st.error("Invalid username or password!")
                    else:
                        st.error("Please fill in all fields!")
        
        with tab2:
            st.subheader("Join SecureBank Pro!")
            with st.form("register_form"):
                new_username = st.text_input("Username", placeholder="Choose a username")
                new_email = st.text_input("Email", placeholder="Enter your email")
                new_password = st.text_input("Password", type="password", placeholder="Create a password")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
                submit_register = st.form_submit_button("Register", use_container_width=True)
                
                if submit_register:
                    if new_username and new_email and new_password and confirm_password:
                        if new_password == confirm_password:
                            success, message = db.register_user(new_username, new_password, new_email)
                            if success:
                                st.success(message)
                            else:
                                st.error(message)
                        else:
                            st.error("Passwords do not match!")
                    else:
                        st.error("Please fill in all fields!")

def show_banking_dashboard():
    """Display main banking dashboard"""
    # Sidebar
    with st.sidebar:
        st.markdown(f"### Welcome, {st.session_state.username}! 👋")
        
        menu_option = st.selectbox(
            "Navigate to:",
            ["🏠 Dashboard", "💳 My Accounts", "💰 Transactions", "🔄 Transfer Money", 
             "➕ Open New Account", "📊 Analytics", "⚙️ Settings"]
        )
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.rerun()
    
    # Main content based on menu selection
    if menu_option == "🏠 Dashboard":
        show_dashboard()
    elif menu_option == "💳 My Accounts":
        show_accounts()
    elif menu_option == "💰 Transactions":
        show_transactions()
    elif menu_option == "🔄 Transfer Money":
        show_transfer()
    elif menu_option == "➕ Open New Account":
        show_new_account()
    elif menu_option == "📊 Analytics":
        show_analytics()
    elif menu_option == "⚙️ Settings":
        show_settings()

def show_dashboard():
    """Display dashboard overview"""
    st.header("🏠 Dashboard Overview")
    
    # Get user accounts
    accounts = db.get_user_accounts(st.session_state.user_id)
    
    if accounts:
        # Calculate metrics
        total_balance = sum(account[2] for account in accounts)
        total_accounts = len(accounts)
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>💰 Total Balance</h3>
                <h2>₹{:,.2f}</h2>
            </div>
            """.format(total_balance), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3>💳 Total Accounts</h3>
                <h2>{}</h2>
            </div>
            """.format(total_accounts), unsafe_allow_html=True)
        
        with col3:
            savings_count = sum(1 for account in accounts if account[1] == 'savings')
            st.markdown("""
            <div class="metric-card">
                <h3>🏦 Savings Accounts</h3>
                <h2>{}</h2>
            </div>
            """.format(savings_count), unsafe_allow_html=True)
        
        with col4:
            current_count = sum(1 for account in accounts if account[1] == 'current')
            st.markdown("""
            <div class="metric-card">
                <h3>🏢 Current Accounts</h3>
                <h2>{}</h2>
            </div>
            """.format(current_count), unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick Actions
        st.subheader("⚡ Quick Actions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💰 Make Deposit", use_container_width=True):
                st.session_state.quick_action = "deposit"
        
        with col2:
            if st.button("💸 Withdraw Money", use_container_width=True):
                st.session_state.quick_action = "withdraw"
        
        with col3:
            if st.button("🔄 Transfer Funds", use_container_width=True):
                st.session_state.quick_action = "transfer"
        
        # Handle quick actions
        if hasattr(st.session_state, 'quick_action'):
            handle_quick_action(accounts)
        
        # Recent transactions
        st.subheader("📋 Recent Transactions")
        if accounts:
            recent_transactions = []
            for account in accounts:
                transactions = db.get_transactions(account[0], 5)
                for txn in transactions:
                    recent_transactions.append([
                        account[0], txn[0], txn[1], txn[4], txn[5]
                    ])
            
            if recent_transactions:
                df = pd.DataFrame(recent_transactions, 
                                columns=['Account', 'Type', 'Amount', 'Date', 'Reference'])
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No recent transactions found.")
        
    else:
        st.info("You don't have any accounts yet. Let's create your first account!")
        if st.button("➕ Open Your First Account", use_container_width=True):
            show_new_account()

def handle_quick_action(accounts):
    """Handle quick actions from dashboard"""
    action = st.session_state.quick_action
    
    if action == "deposit":
        st.subheader("💰 Quick Deposit")
        with st.form("quick_deposit"):
            account_options = [f"{acc[0]} - {acc[3]} (Balance: ₹{acc[2]:,.2f})" for acc in accounts]
            selected_account = st.selectbox("Select Account", account_options)
            amount = st.number_input("Amount to Deposit", min_value=1.0, step=1.0)
            
            if st.form_submit_button("Deposit"):
                account_number = selected_account.split(" - ")[0]
                account = db.get_account_details(account_number)
                if account:
                    new_balance = account[2] + amount
                    db.update_balance(account_number, new_balance)
                    ref_num = db.add_transaction(account_number, "deposit", amount, new_balance, "Quick deposit")
                    st.success(f"Deposit successful! Reference: {ref_num}")
                    del st.session_state.quick_action
                    st.rerun()
    
    elif action == "withdraw":
        st.subheader("💸 Quick Withdrawal")
        with st.form("quick_withdraw"):
            account_options = [f"{acc[0]} - {acc[3]} (Balance: ₹{acc[2]:,.2f})" for acc in accounts]
            selected_account = st.selectbox("Select Account", account_options)
            amount = st.number_input("Amount to Withdraw", min_value=1.0, step=1.0)
            
            if st.form_submit_button("Withdraw"):
                account_number = selected_account.split(" - ")[0]
                account = db.get_account_details(account_number)
                if account and account[2] >= amount:
                    new_balance = account[2] - amount
                    db.update_balance(account_number, new_balance)
                    ref_num = db.add_transaction(account_number, "withdrawal", amount, new_balance, "Quick withdrawal")
                    st.success(f"Withdrawal successful! Reference: {ref_num}")
                    del st.session_state.quick_action
                    st.rerun()
                else:
                    st.error("Insufficient balance!")

def show_accounts():
    """Display user accounts"""
    st.header("💳 My Accounts")
    
    accounts = db.get_user_accounts(st.session_state.user_id)
    
    if accounts:
        for account in accounts:
            st.markdown(f"""
            <div class="account-card">
                <h3>🏦 {account[3]}</h3>
                <p><strong>Account Number:</strong> {account[0]}</p>
                <p><strong>Account Type:</strong> {account[1].title()}</p>
                <p><strong>Phone:</strong> {account[4]}</p>
                <p><strong>Address:</strong> {account[5]}</p>
                <p><strong>Status:</strong> {account[7].title()}</p>
                <div class="balance-display">₹{account[2]:,.2f}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Action buttons for each account
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"💰 Deposit", key=f"dep_{account[0]}"):
                    show_deposit_form(account[0])
            with col2:
                if st.button(f"💸 Withdraw", key=f"with_{account[0]}"):
                    show_withdraw_form(account[0])
            with col3:
                if st.button(f"📋 Transactions", key=f"txn_{account[0]}"):
                    show_account_transactions(account[0])
    else:
        st.info("No accounts found. Create your first account!")

def show_deposit_form(account_number):
    """Show deposit form for specific account"""
    st.subheader(f"💰 Deposit to Account {account_number}")
    
    with st.form(f"deposit_{account_number}"):
        amount = st.number_input("Amount to Deposit", min_value=1.0, step=1.0)
        description = st.text_input("Description (Optional)", placeholder="Purpose of deposit")
        
        if st.form_submit_button("Deposit"):
            account = db.get_account_details(account_number)
            if account:
                new_balance = account[2] + amount
                db.update_balance(account_number, new_balance)
                ref_num = db.add_transaction(account_number, "deposit", amount, new_balance, 
                                           description or "Cash deposit")
                st.success(f"Deposit successful! Reference: {ref_num}")
                st.rerun()

def show_withdraw_form(account_number):
    """Show withdrawal form for specific account"""
    st.subheader(f"💸 Withdraw from Account {account_number}")
    
    account = db.get_account_details(account_number)
    if account:
        st.info(f"Available Balance: ₹{account[2]:,.2f}")
        
        with st.form(f"withdraw_{account_number}"):
            amount = st.number_input("Amount to Withdraw", min_value=1.0, max_value=account[2], step=1.0)
            description = st.text_input("Description (Optional)", placeholder="Purpose of withdrawal")
            
            if st.form_submit_button("Withdraw"):
                if amount <= account[2]:
                    new_balance = account[2] - amount
                    db.update_balance(account_number, new_balance)
                    ref_num = db.add_transaction(account_number, "withdrawal", amount, new_balance, 
                                               description or "Cash withdrawal")
                    st.success(f"Withdrawal successful! Reference: {ref_num}")
                    st.rerun()
                else:
                    st.error("Insufficient balance!")

def show_account_transactions(account_number):
    """Show transactions for specific account"""
    st.subheader(f"📋 Transaction History - {account_number}")
    
    transactions = db.get_transactions(account_number, 100)
    
    if transactions:
        df = pd.DataFrame(transactions, columns=[
            'Type', 'Amount', 'Balance After', 'Description', 'Date', 'Reference'
        ])
        
        # Format the dataframe
        df['Amount'] = df['Amount'].apply(lambda x: f"₹{x:,.2f}")
        df['Balance After'] = df['Balance After'].apply(lambda x: f"₹{x:,.2f}")
        df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d %H:%M')
        
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No transactions found for this account.")

def show_transactions():
    """Display transaction management page"""
    st.header("💰 Transaction Management")
    
    accounts = db.get_user_accounts(st.session_state.user_id)
    
    if accounts:
        tab1, tab2 = st.tabs(["📋 Transaction History", "🔍 Search Transactions"])
        
        with tab1:
            # Account selector
            account_options = ["All Accounts"] + [f"{acc[0]} - {acc[3]}" for acc in accounts]
            selected_account = st.selectbox("Select Account", account_options)
            
            if selected_account == "All Accounts":
                all_transactions = []
                for account in accounts:
                    transactions = db.get_transactions(account[0], 50)
                    for txn in transactions:
                        all_transactions.append([
                            account[0], account[3], txn[0], txn[1], txn[2], txn[3], txn[4], txn[5]
                        ])
                
                if all_transactions:
                    df = pd.DataFrame(all_transactions, columns=[
                        'Account Number', 'Account Holder', 'Type', 'Amount', 'Balance After', 
                        'Description', 'Date', 'Reference'
                    ])
                    df['Amount'] = df['Amount'].apply(lambda x: f"₹{x:,.2f}")
                    df['Balance After'] = df['Balance After'].apply(lambda x: f"₹{x:,.2f}")
                    st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                account_number = selected_account.split(" - ")[0]
                show_account_transactions(account_number)
        
        with tab2:
            st.subheader("🔍 Search Transactions")
            
            col1, col2 = st.columns(2)
            with col1:
                search_account = st.selectbox("Account", ["All"] + [acc[0] for acc in accounts])
                transaction_type = st.selectbox("Type", ["All", "deposit", "withdrawal", "transfer_in", "transfer_out"])
            
            with col2:
                date_from = st.date_input("From Date", value=datetime.now() - timedelta(days=30))
                date_to = st.date_input("To Date", value=datetime.now())
            
            min_amount = st.number_input("Minimum Amount", min_value=0.0, value=0.0)
            max_amount = st.number_input("Maximum Amount", min_value=0.0, value=100000.0)
            
            if st.button("Search"):
                # Implement search logic here
                st.info("Search functionality will be implemented based on the criteria above.")

def show_transfer():
    """Display money transfer page"""
    st.header("🔄 Transfer Money")
    
    accounts = db.get_user_accounts(st.session_state.user_id)
    
    if len(accounts) >= 1:
        with st.form("transfer_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("From Account")
                from_options = [f"{acc[0]} - {acc[3]} (₹{acc[2]:,.2f})" for acc in accounts]
                from_account = st.selectbox("Select Source Account", from_options)
                
            with col2:
                st.subheader("To Account")
                to_account = st.text_input("Destination Account Number", placeholder="Enter account number")
            
            amount = st.number_input("Transfer Amount", min_value=1.0, step=1.0)
            description = st.text_input("Description (Optional)", placeholder="Purpose of transfer")
            
            if st.form_submit_button("Transfer Money", use_container_width=True):
                from_acc_number = from_account.split(" - ")[0]
                
                if from_acc_number != to_account:
                    success, message = db.transfer_money(from_acc_number, to_account, amount)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Cannot transfer to the same account!")
    else:
        st.info("You need at least one account to make transfers.")

def show_new_account():
    """Display new account creation page"""
    st.header("➕ Open New Account")
    
    with st.form("new_account_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            account_holder_name = st.text_input("Account Holder Name*", placeholder="Full legal name")
            phone_number = st.text_input("Phone Number*", placeholder="Mobile number")
            account_type = st.selectbox("Account Type*", ["savings", "current"])
        
        with col2:
            address = st.text_area("Address*", placeholder="Complete address")
            initial_deposit = st.number_input("Initial Deposit", min_value=0.0, step=100.0, 
                                            help="Minimum ₹500 for Savings, ₹1000 for Current")
        
        terms_accepted = st.checkbox("I accept the terms and conditions*")
        
        if st.form_submit_button("Create Account", use_container_width=True):
            if all([account_holder_name, phone_number, address, terms_accepted]):
                min_deposit = 500 if account_type == "savings" else 1000
                if initial_deposit >= min_deposit:
                    success, result = db.create_account(
                        st.session_state.user_id, account_type, account_holder_name, 
                        phone_number, address, initial_deposit
                    )
                    if success:
                        st.success(f"Account created successfully! Account Number: {result}")
                        st.balloons()
                    else:
                        st.error(f"Error creating account: {result}")
                else:
                    st.error(f"Minimum deposit required: ₹{min_deposit}")
            else:
                st.error("Please fill in all required fields and accept terms!")

def show_analytics():
    """Display analytics and insights page"""
    st.header("📊 Analytics & Insights")
    
    accounts = db.get_user_accounts(st.session_state.user_id)
    
    if accounts:
        # Balance distribution
        st.subheader("💰 Account Balance Distribution")
        
        balance_data = []
        for account in accounts:
            balance_data.append({
                'Account': f"{account[0][:8]}...",
                'Type': account[1].title(),
                'Balance': account[2],
                'Holder': account[3]
            })
        
        df_balance = pd.DataFrame(balance_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart for account types
            type_counts = df_balance['Type'].value_counts()
            fig_pie = px.pie(values=type_counts.values, names=type_counts.index, 
                           title="Account Types Distribution")
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Bar chart for balances
            fig_bar = px.bar(df_balance, x='Account', y='Balance', color='Type',
                           title="Account Balances", 
                           labels={'Balance': 'Balance (₹)'})
            fig_bar.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Transaction trends
        st.subheader("📈 Transaction Trends (Last 30 Days)")
        
        # Collect transaction data
        all_transactions = []
        for account in accounts:
            transactions = db.get_transactions(account[0], 100)
            for txn in transactions:
                txn_date = datetime.strptime(txn[4], '%Y-%m-%d %H:%M:%S')
                if txn_date >= datetime.now() - timedelta(days=30):
                    all_transactions.append({
                        'Date': txn_date.date(),
                        'Type': txn[0],
                        'Amount': txn[1],
                        'Account': account[0]
                    })
        
        if all_transactions:
            df_txn = pd.DataFrame(all_transactions)
            
            # Daily transaction volume
            daily_volume = df_txn.groupby('Date')['Amount'].sum().reset_index()
            fig_line = px.line(daily_volume, x='Date', y='Amount', 
                             title="Daily Transaction Volume",
                             labels={'Amount': 'Amount (₹)'})
            st.plotly_chart(fig_line, use_container_width=True)
            
            # Transaction type breakdown
            type_summary = df_txn.groupby('Type')['Amount'].agg(['count', 'sum']).reset_index()
            type_summary.columns = ['Transaction Type', 'Count', 'Total Amount']
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📊 Transaction Summary")
                st.dataframe(type_summary, hide_index=True)
            
            with col2:
                # Monthly spending pattern
                if len(all_transactions) > 0:
                    withdrawal_data = df_txn[df_txn['Type'].isin(['withdrawal', 'transfer_out'])]
                    if not withdrawal_data.empty:
                        monthly_spending = withdrawal_data.groupby(withdrawal_data['Date'].dt.to_period('M'))['Amount'].sum()
                        st.metric("💸 Monthly Spending", f"₹{monthly_spending.iloc[-1]:,.2f}" if len(monthly_spending) > 0 else "₹0")
                    
                    deposit_data = df_txn[df_txn['Type'].isin(['deposit', 'transfer_in'])]
                    if not deposit_data.empty:
                        monthly_income = deposit_data.groupby(deposit_data['Date'].dt.to_period('M'))['Amount'].sum()
                        st.metric("💰 Monthly Income", f"₹{monthly_income.iloc[-1]:,.2f}" if len(monthly_income) > 0 else "₹0")
        else:
            st.info("No transactions in the last 30 days to analyze.")
    
    else:
        st.info("No accounts found to analyze.")

def show_settings():
    """Display settings page"""
    st.header("⚙️ Settings")
    
    tab1, tab2, tab3 = st.tabs(["👤 Profile", "🔐 Security", "🎨 Preferences"])
    
    with tab1:
        st.subheader("Profile Information")
        st.info("Profile management features coming soon!")
        
        # Placeholder for profile settings
        st.text_input("Display Name", value=st.session_state.username, disabled=True)
        st.text_input("Email", placeholder="user@example.com", disabled=True)
        st.text_input("Phone", placeholder="+91 XXXXX XXXXX", disabled=True)
    
    with tab2:
        st.subheader("Security Settings")
        
        with st.form("change_password"):
            st.text_input("Current Password", type="password")
            st.text_input("New Password", type="password")
            st.text_input("Confirm New Password", type="password")
            
            if st.form_submit_button("Change Password"):
                st.info("Password change functionality will be implemented.")
        
        st.subheader("Two-Factor Authentication")
        st.checkbox("Enable 2FA (Coming Soon)", disabled=True)
    
    with tab3:
        st.subheader("App Preferences")
        
        theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
        currency = st.selectbox("Currency", ["INR (₹)", "USD ($)", "EUR (€)"])
        language = st.selectbox("Language", ["English", "Hindi", "Tamil", "Telugu"])
        
        if st.button("Save Preferences"):
            st.success("Preferences saved!")

if __name__ == "__main__":
    main()
