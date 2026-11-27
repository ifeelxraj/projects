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
    pin = *next;
    std::cout << "Pin changed successfully.\n";
}

void withdraw(atm::Account& account) {
    const auto text = prompt("Amount to withdraw: ");
    if (!text) return;
    const auto amount = atm::parse_amount(*text);
    if (!amount || *amount == 0) {
        std::cout << "Enter a positive amount, for example 12.50.\n";
        return;
    }
    if (account.withdraw(*amount) != atm::Result::ok) {
        std::cout << "Insufficient balance.\n";
        return;
    }
    std::cout << "Withdrawal amount: " << atm::format_amount(*amount) << '\n';
    std::cout << "Remaining balance: " << atm::format_amount(account.balance()) << '\n';
}

void show_menu(atm::Account& account, std::string& pin) {
    const auto choice = prompt("1) Check balance\n2) Withdraw\n3) Change PIN\nChoice: ");
    if (!choice) return;
    if (*choice == "1") std::cout << "Balance: " << atm::format_amount(account.balance()) << '\n';
    else if (*choice == "2") withdraw(account);
    else if (*choice == "3") change_pin(pin);
    else std::cout << "Invalid choice.\n";
}

}  // namespace

int main() {
    atm::Account account{1'000'000};
    auto pin = choose_pin();
    if (pin && authenticate(*pin)) show_menu(account, *pin);
}
