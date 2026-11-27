#include "atm/account.hpp"
#include "atm/pin.hpp"

#include <iostream>
#include <string>
using namespace std;

string pin = "2486";
atm::Account account{1'000'000};

void pinchange()
{
    string enteredpin, newpin;
    cout << "Enter Current Pin: ";
    if (!(cin >> enteredpin) || enteredpin != pin)
    {
        cout << "PIN not changed.\n";
        return;
    }
    cout << "Generate New Pin: ";
    if (!(cin >> newpin) || !atm::valid_pin(newpin) || newpin == pin)
    {
        cout << "Choose a different four-digit PIN.\n";
        return;
    }
    pin = newpin;
    cout << "Pin changed successfully\n";
}

void checkbalance()
{
    cout << "Balance: " << atm::format_amount(account.balance()) << "\n";
}

void withdraw()
{
    string text;
    cout << "Enter amount to withdraw: ";
    if (!(cin >> text)) return;
    const auto amount = atm::parse_amount(text);
    if (!amount || *amount == 0)
    {
        cout << "Enter a positive amount, for example 12.50.\n";
        return;
    }
    if (account.withdraw(*amount) != atm::Result::ok)
    {
        cout << "Insufficient balance.\n";
        return;
    }
    cout << "Withdrawal amount: " << atm::format_amount(*amount) << "\n";
    cout << "Remaining balance: " << atm::format_amount(account.balance()) << "\n";
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
        string entered;
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
