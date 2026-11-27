#include "atm/account.hpp"
#include "atm/pin.hpp"

#include <iostream>
#include <optional>
#include <string>
#include <string_view>

namespace {

std::optional<std::string> prompt(std::string_view question) {
    std::cout << question << std::flush;
    std::string line;
    if (!std::getline(std::cin, line)) return std::nullopt;
    const auto first = line.find_first_not_of(" \t\r");
    if (first == line.npos) return std::string{};
    return line.substr(first, line.find_last_not_of(" \t\r") - first + 1);
}

std::optional<std::string> choose_pin() {
    std::cout << "Local simulation. Use a made-up PIN; input is visible.\n";
    for (;;) {
        auto pin = prompt("Choose a four-digit demo PIN: ");
        if (!pin || atm::valid_pin(*pin)) return pin;
        std::cout << "Use exactly four digits (0-9).\n";
    }
}

bool authenticate(std::string_view pin) {
    for (int attempt = 0; attempt < 3; ++attempt) {
        const auto entered = prompt("Enter PIN: ");
        if (!entered) return false;
        if (*entered == pin) return true;
        std::cout << "Wrong PIN.\n";
    }
    std::cout << "Too many attempts. Session ended.\n";
    return false;
}

void change_pin(std::string& pin) {
    const auto current = prompt("Current PIN: ");
    if (!current || *current != pin) {
        std::cout << "PIN not changed.\n";
        return;
    }
    const auto next = prompt("New PIN: ");
    if (!next || !atm::valid_pin(*next) || *next == pin) {
        std::cout << "Choose a different four-digit PIN.\n";
        return;
    }
    const auto confirmation = prompt("Repeat new PIN: ");
    if (!confirmation || *confirmation != *next) {
        std::cout << "PIN not changed: confirmation did not match.\n";
        return;
    }
    pin = *next;
    std::cout << "Pin changed successfully.\n";
}

void transact(atm::Account& account, atm::Movement type) {
    const bool debit = type == atm::Movement::withdrawal;
    const auto text = prompt(debit ? "Amount to withdraw: " : "Amount to deposit: ");
    if (!text) return;
    const auto amount = atm::parse_amount(*text);
    if (!amount) {
        std::cout << "Enter a positive amount, for example 12.50.\n";
        return;
    }
    const auto result = debit ? account.withdraw(*amount) : account.deposit(*amount);
    switch (result) {
        case atm::Result::zero_amount:
            std::cout << "Enter a positive amount, for example 12.50.\n";
            return;
        case atm::Result::insufficient_funds:
            std::cout << "Insufficient balance.\n";
            return;
        case atm::Result::balance_limit:
            std::cout << "Deposit would exceed the balance limit.\n";
            return;
        case atm::Result::ok: break;
    }
    std::cout << (debit ? "Withdrawal amount: " : "Deposit amount: ") << atm::format_amount(*amount) << '\n';
    std::cout << "Remaining balance: " << atm::format_amount(account.balance()) << '\n';
}

void show_menu(atm::Account& account, std::string& pin) {
    for (;;) {
        const auto choice = prompt("1) Check balance\n2) Withdraw\n3) Change PIN\n4) Deposit\n0) Exit\nChoice: ");
        if (!choice || *choice == "0") return;
        if (*choice == "1") std::cout << "Balance: " << atm::format_amount(account.balance()) << '\n';
        else if (*choice == "2") transact(account, atm::Movement::withdrawal);
        else if (*choice == "3") change_pin(pin);
        else if (*choice == "4") transact(account, atm::Movement::deposit);
        else std::cout << "Invalid choice.\n";
    }
}

}  // namespace

int main() {
    atm::Account account{1'000'000};
    auto pin = choose_pin();
    if (pin && authenticate(*pin)) show_menu(account, *pin);
}
