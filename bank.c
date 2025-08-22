#include <stdio.h>
#include <string.h>

#define MAX_ACCOUNTS 100
#define DATA_FILE "accounts.dat"

typedef struct {
    char accountNumber[20];
    double balance;
} BankAccount;

BankAccount accounts[MAX_ACCOUNTS];
int accountCount = 0;

void saveAccounts() {
    FILE *file = fopen(DATA_FILE, "wb");
    if (file != NULL) {
        fwrite(&accountCount, sizeof(int), 1, file);
        fwrite(accounts, sizeof(BankAccount), accountCount, file);
        fclose(file);
    } else {
        printf("Error saving accounts.\n");
    }
}

void loadAccounts() {
    FILE *file = fopen(DATA_FILE, "rb");
    if (file != NULL) {
        fread(&accountCount, sizeof(int), 1, file);
        fread(accounts, sizeof(BankAccount), accountCount, file);
        fclose(file);
    } else {
        printf("No previous data found.\n");
    }
}

void addAccount(char *accountNumber) {
    strcpy(accounts[accountCount].accountNumber, accountNumber);
    accounts[accountCount].balance = 0.0;
    accountCount++;
}

void depositMoney(char *accountNumber, double amount) {
    for (int i = 0; i < accountCount; i++) {
        if (strcmp(accounts[i].accountNumber, accountNumber) == 0) {
            accounts[i].balance += amount;
            printf("Deposited %.2f to account %s\n", amount, accountNumber);
            return;
        }
    }
    printf("Account not found.\n");
}

void checkBalance(char *accountNumber) {
    for (int i = 0; i < accountCount; i++) {
        if (strcmp(accounts[i].accountNumber, accountNumber) == 0) {
            printf("Balance for account %s: %.2f\n", accountNumber, accounts[i].balance);
            return;
        }
    }
    printf("Account not found.\n");
}

int main() {
    loadAccounts();

    char accountNumber[20];
    double amount;
    int choice;

    while (1) {
        printf("1. Add Account\n");
        printf("2. Deposit Money\n");
        printf("3. Check Balance\n");
        printf("4. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("Enter account number: ");
                scanf("%s", accountNumber);
                addAccount(accountNumber);
                break;
            case 2:
                printf("Enter account number: ");
                scanf("%s", accountNumber);
                printf("Enter amount to deposit: ");
                scanf("%lf", &amount);
                depositMoney(accountNumber, amount);
                break;
            case 3:
                printf("Enter account number: ");
                scanf("%s", accountNumber);
                checkBalance(accountNumber);
                break;
            case 4:
                saveAccounts();
                return 0;
            default:
                printf("Invalid choice. Please try again.\n");
        }
    }

    return 0;
}