#include <iostream>
#include <string>
#include <map>
#include <cstdlib>
#include <ctime>
#include <limits>

using namespace std;

class BankAccount {
    string name;
    string address;
    char accountType;
    int balance;

public:
    // Default constructor
    BankAccount() : name(""), address(""), accountType('s'), balance(0) {}

    // Parameterized constructor
    BankAccount(const string &name, const string &address, char accountType, int balance)
        : name(name), address(address), accountType(accountType), balance(balance) {}

    void depositMoney(int amount) {
        if (amount > 0) {
            balance += amount;
            cout << "Deposit successful. New balance: " << balance << endl;
        } else {
            cout << "Invalid deposit amount." << endl;
        }
    }

    bool withdrawMoney(int amount) {
        if (amount > balance) {
            cout << "Insufficient balance. Withdrawal failed." << endl;
            return false;
        } else if (amount <= 0) {
            cout << "Invalid withdrawal amount." << endl;
            return false;
        } else {
            balance -= amount;
            cout << "Withdrawal successful. Remaining balance: " << balance << endl;
            return true;
        }
    }

    void displayAccount() const {
        cout << "Name: " << name << endl;
        cout << "Address: " << address << endl;
        cout << "Account Type: " << (accountType == 's' ? "Savings" : "Current") << endl;
        cout << "Balance: " << balance << endl;
    }

    string getName() const {
        return name;
    }
};

class Bank {
    map<int, BankAccount> accounts;

    int generateAccountNumber() {
        srand(time(0));
        int accountNumber;
        do {
            accountNumber = rand() % 900000 + 100000;  // Generate a 6-digit number
        } while (accounts.find(accountNumber) != accounts.end());
        return accountNumber;
    }

public:
    void openAccount() {
        string name, address;
        char accountType;
        int initialDeposit;

        cout << "Enter your full name: ";
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
        getline(cin, name);
        cout << "Enter your address: ";
        getline(cin, address);
        cout << "What type of account do you want to open? Savings (s) or Current (c): ";
        cin >> accountType;
        cout << "Enter amount for deposit: ";
        cin >> initialDeposit;

        if (initialDeposit < 0) {
            cout << "Initial deposit cannot be negative. Account not created." << endl;
        } else {
            int accountNumber = generateAccountNumber();
            accounts[accountNumber] = BankAccount(name, address, accountType, initialDeposit);
            cout << "Your account has been created. Your account number is: " << accountNumber << endl;
        }
    }

    void depositMoney() {
        int accountNumber;
        int amount;
        cout << "Enter your account number: ";
        cin >> accountNumber;

        if (accounts.find(accountNumber) != accounts.end()) {
            cout << "Enter amount to deposit: ";
            cin >> amount;
            accounts[accountNumber].depositMoney(amount);
        } else {
            cout << "Account not found." << endl;
        }
    }

    void withdrawMoney() {
        int accountNumber;
        int amount;
        cout << "Enter your account number: ";
        cin >> accountNumber;

        if (accounts.find(accountNumber) != accounts.end()) {
            cout << "Enter amount to withdraw: ";
            cin >> amount;
            accounts[accountNumber].withdrawMoney(amount);
        } else {
            cout << "Account not found." << endl;
        }
    }

    void displayAccount() {
        int accountNumber;
        cout << "Enter your account number: ";
        cin >> accountNumber;

        if (accounts.find(accountNumber) != accounts.end()) {
            accounts[accountNumber].displayAccount();
        } else {
            cout << "Account not found." << endl;
        }
    }
};

int main() {
    Bank bank;
    int choice;
    char cont;

    do {
        system("cls");
        cout << "01) Open account\n";
        cout << "02) Deposit money\n";
        cout << "03) Withdraw money\n";
        cout << "04) Display account\n";
        cout << "05) Exit\n";
        cout << "Please select an option: ";
        cin >> choice;

        switch (choice) {
            case 1:
                bank.openAccount();
                break;
            case 2:
                bank.depositMoney();
                break;
            case 3:
                bank.withdrawMoney();
                break;
            case 4:
                bank.displayAccount();
                break;
            case 5:
                cout << "Exiting..." << endl;
                return 0;
            default:
                cout << "Invalid option, please try again." << endl;
        }

        cout << "\nDo you want to select the next step? Press 'y' for yes, 'n' for no: ";
        cin >> cont;
    } while (cont == 'y' || cont == 'Y');

    return 0;
}
