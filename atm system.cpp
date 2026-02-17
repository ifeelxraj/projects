#include <iostream>
using namespace std;

int pin = 2486;
int balance = 10000;

void forgetpin()
{
    int newpin;
    cout << "OTP will be sent to your linked mobile number\n";
    cout << "Generate New Pin: ";
    cin >> newpin;
    if (pin == newpin)
    {
        cout << "Invalid Pin, new pin cannot be same as old pin\n";
    }
    else
    {
        pin = newpin;
        cout << "Pin changed successfully\n";
    }
}

void pinchange()
{
    int enteredpin, newpin;
    cout << "Enter Current Pin: ";
    cin >> enteredpin;
    if (pin == enteredpin)
    {
        cout << "Generate New Pin: ";
        cin >> newpin;
        if (pin == newpin)
        {
            cout << "Invalid Pin, new pin cannot be same as old pin\n";
        }
        else
        {
            pin = newpin;
            cout << "Pin changed successfully\n";
        }
    }
    else
    {
        cout << "Wrong Pin, Enter correct pin\n";
        int choice;
        cout << "1) Forget Pin\n2) Re-enter pin\n";
        cin >> choice;
        switch (choice)
        {
        case 1:
            forgetpin();
            break;
        case 2:
            pinchange();
            break;
        default:
            cout << "Invalid choice\n";
        }
    }
}

void checkbalance()
{
    cout << "Balance: " << balance << "\n";
}

void withdraw()
{
    int amount;
    cout << "Enter amount to withdraw: ";
    cin >> amount;
    
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
    int epin;
    cout << "Enter Pin: ";
    cin >> epin;
    
    if (pin == epin)
    {
        showMenu();
    }
    else
    {   
        int choice;
        cout << "Wrong Pin\n";
        cout << "1) Forget Pin\n2) Re-enter Pin\n";
        cout << "Enter choice: ";
        cin >> choice;
        
        switch(choice)
        {
            case 1: 
                forgetpin();
                break;
        
            case 2: 
                login();  
                break;
                
            default:
                cout << "Invalid Choice\n";
                break;
        }
    }
}

int main()
{
    login();
    return 0;
}
