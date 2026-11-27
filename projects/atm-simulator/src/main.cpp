#include <iostream>
using namespace std;

int pin = 2486;
int balance = 10000;

void pinchange()
{
    int enteredpin, newpin;
    cout << "Enter Current Pin: ";
    if (!(cin >> enteredpin) || enteredpin != pin)
    {
        cout << "PIN not changed.\n";
        return;
    }
    cout << "Generate New Pin: ";
    if (!(cin >> newpin) || newpin == pin)
    {
        cout << "Choose a different PIN.\n";
        return;
    }
    pin = newpin;
    cout << "Pin changed successfully\n";
}

void checkbalance()
{
    cout << "Balance: " << balance << "\n";
}

void withdraw()
{
    int amount;
    cout << "Enter amount to withdraw: ";
    if (!(cin >> amount) || amount <= 0)
    {
        cout << "Enter a positive amount.\n";
        return;
    }
    
    if (amount > balance)
    {
        cout << "Insufficient Balance\n";
    }
    else
    {
        cout << "Withdraw successful\n";
        balance = balance - amount;
        cout << "Withdrawal amount: " << amount << "\n";
        cout << "Remaining balance: " << balance << "\n";
    }
}

void showMenu()
{
    int choice;
    cout << "1) Check Balance\n2) Withdraw Money\n3) Generate New Pin\n";
    cin >> choice;
    
    switch (choice)
    {
        case 1: 
            checkbalance();
            break;
        
        case 2: 
            withdraw();
            break;
            
        case 3: 
            pinchange();
            break;
    
        default: 
            cout << "Invalid Choice\n";
            break;
    }
}

void login()
{
    for (int attempt = 0; attempt < 3; ++attempt)
    {
        int entered;
        cout << "Enter Pin: ";
        if (!(cin >> entered)) return;
        if (pin == entered)
        {
            showMenu();
            return;
        }
        cout << "Wrong PIN.\n";
    }
    cout << "Too many attempts. Session ended.\n";
}

int main()
{
    login();
    return 0;
}
