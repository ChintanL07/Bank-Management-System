"""
Demo Data Generator for SecureBank Pro
This script creates sample users and accounts for demonstration purposes.
"""

import sqlite3
import bcrypt
import random
from datetime import datetime, timedelta

def create_demo_data():
    """Create demo users, accounts, and transactions"""
    
    # Database connection
    conn = sqlite3.connect("bank_system.db")
    cursor = conn.cursor()
    
    try:
        # Create demo users
        demo_users = [
            ("john_doe", "password123", "john.doe@email.com"),
            ("jane_smith", "mypassword", "jane.smith@email.com"),
            ("alice_johnson", "securepass", "alice.j@email.com"),
            ("bob_wilson", "bobpass456", "bob.wilson@email.com")
        ]
        
        print("Creating demo users...")
        user_ids = []
        
        for username, password, email in demo_users:
            # Check if user already exists
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                user_ids.append(existing_user[0])
                print(f"User {username} already exists, skipping...")
                continue
            
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute(
                "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
                (username, password_hash, email)
            )
            user_ids.append(cursor.lastrowid)
            print(f"Created user: {username}")
        
        # Create demo accounts
        demo_accounts = [
            # John Doe's accounts
            (user_ids[0], "savings", "John Doe", "+91 9876543210", "123 Main St, Mumbai", 25000.00),
            (user_ids[0], "current", "John Doe", "+91 9876543210", "123 Main St, Mumbai", 50000.00),
            
            # Jane Smith's accounts
            (user_ids[1], "savings", "Jane Smith", "+91 8765432109", "456 Park Ave, Delhi", 35000.00),
            
            # Alice Johnson's accounts
            (user_ids[2], "savings", "Alice Johnson", "+91 7654321098", "789 Oak Rd, Bangalore", 18000.00),
            (user_ids[2], "current", "Alice Johnson", "+91 7654321098", "789 Oak Rd, Bangalore", 75000.00),
            
            # Bob Wilson's accounts
            (user_ids[3], "savings", "Bob Wilson", "+91 6543210987", "321 Pine St, Chennai", 42000.00),
        ]
        
        print("\nCreating demo accounts...")
        account_numbers = []
        
        for user_id, acc_type, name, phone, address, balance in demo_accounts:
            # Generate account number
            account_number = f"ACC{random.randint(100000000, 999999999)}"
            
            cursor.execute('''
                INSERT INTO accounts 
                (account_number, user_id, account_type, balance, account_holder_name, phone_number, address)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (account_number, user_id, acc_type, balance, name, phone, address))
            
            account_numbers.append((account_number, balance))
            print(f"Created {acc_type} account: {account_number} for {name}")
        
        # Create demo transactions
        print("\nCreating demo transactions...")
        
        for i, (account_number, current_balance) in enumerate(account_numbers):
            # Create some random transactions for each account
            transaction_types = ["deposit", "withdrawal"]
            
            # Generate 5-10 random transactions per account
            num_transactions = random.randint(5, 10)
            balance = current_balance
            
            for j in range(num_transactions):
                # Random date within last 30 days
                days_ago = random.randint(1, 30)
                transaction_date = datetime.now() - timedelta(days=days_ago)
                
                transaction_type = random.choice(transaction_types)
                
                if transaction_type == "deposit":
                    amount = random.randint(1000, 10000)
                    balance += amount
                    description = random.choice([
                        "Salary credit", "Online transfer", "Cash deposit", 
                        "Dividend payment", "Interest credit"
                    ])
                else:  # withdrawal
                    max_withdrawal = min(5000, balance * 0.1)  # Max 10% of balance or 5000
                    if max_withdrawal > 100:
                        amount = random.randint(100, int(max_withdrawal))
                        balance -= amount
                        description = random.choice([
                            "ATM withdrawal", "Online purchase", "Bill payment",
                            "Cash withdrawal", "EMI deduction"
                        ])
                    else:
                        continue  # Skip if balance too low
                
                # Generate reference number
                reference_number = f"TXN{random.randint(1000000000, 9999999999)}"
                
                cursor.execute('''
                    INSERT INTO transactions 
                    (account_number, transaction_type, amount, balance_after, description, 
                     reference_number, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (account_number, transaction_type, amount, balance, description, 
                      reference_number, transaction_date))
            
            # Update final balance
            cursor.execute("UPDATE accounts SET balance = ? WHERE account_number = ?", 
                         (balance, account_number))
            
            print(f"Created {num_transactions} transactions for account {account_number}")
        
        # Create some transfer transactions
        print("\nCreating demo transfers...")
        if len(account_numbers) >= 2:
            for _ in range(3):  # Create 3 demo transfers
                from_acc = random.choice(account_numbers)[0]
                to_acc = random.choice(account_numbers)[0]
                
                if from_acc != to_acc:
                    # Get current balances
                    cursor.execute("SELECT balance FROM accounts WHERE account_number = ?", (from_acc,))
                    from_balance = cursor.fetchone()[0]
                    
                    cursor.execute("SELECT balance FROM accounts WHERE account_number = ?", (to_acc,))
                    to_balance = cursor.fetchone()[0]
                    
                    # Transfer amount (max 5000 or 10% of balance)
                    max_transfer = min(5000, from_balance * 0.1)
                    if max_transfer > 500:
                        amount = random.randint(500, int(max_transfer))
                        
                        new_from_balance = from_balance - amount
                        new_to_balance = to_balance + amount
                        
                        # Update balances
                        cursor.execute("UPDATE accounts SET balance = ? WHERE account_number = ?", 
                                     (new_from_balance, from_acc))
                        cursor.execute("UPDATE accounts SET balance = ? WHERE account_number = ?", 
                                     (new_to_balance, to_acc))
                        
                        # Create transaction records
                        days_ago = random.randint(1, 15)
                        transfer_date = datetime.now() - timedelta(days=days_ago)
                        ref_num = f"TXN{random.randint(1000000000, 9999999999)}"
                        
                        cursor.execute('''
                            INSERT INTO transactions 
                            (account_number, transaction_type, amount, balance_after, description, 
                             reference_number, timestamp)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        ''', (from_acc, "transfer_out", amount, new_from_balance, 
                              f"Transfer to {to_acc}", ref_num, transfer_date))
                        
                        cursor.execute('''
                            INSERT INTO transactions 
                            (account_number, transaction_type, amount, balance_after, description, 
                             reference_number, timestamp)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        ''', (to_acc, "transfer_in", amount, new_to_balance, 
                              f"Transfer from {from_acc}", ref_num, transfer_date))
                        
                        print(f"Created transfer: {from_acc} → {to_acc} (₹{amount:,.2f})")
        
        conn.commit()
        print("\n✅ Demo data created successfully!")
        print("\n📋 Demo Login Credentials:")
        print("=" * 40)
        for username, password, email in demo_users:
            print(f"Username: {username}")
            print(f"Password: {password}")
            print(f"Email: {email}")
            print("-" * 30)
        
        print("\n🏦 Demo accounts and transactions have been created!")
        print("You can now login to the app and explore the features.")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error creating demo data: {e}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    print("🏦 SecureBank Pro - Demo Data Generator")
    print("=" * 50)
    
    response = input("This will create demo users and accounts. Continue? (y/n): ")
    if response.lower() in ['y', 'yes']:
        create_demo_data()
    else:
        print("Demo data creation cancelled.")
