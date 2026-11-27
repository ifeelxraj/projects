#include "atm/account.hpp"
#include "check.hpp"

#include <algorithm>
#include <random>

int main() {
    // Reconcile an independent running total AND the retained statement after
    // every action, including declines. Fixed seed makes failures repeatable.
    std::mt19937 input(42);
    constexpr atm::Cents opening = 1000;
    atm::Account account(opening);
    atm::Cents credits = 0, debits = 0;
    std::size_t accepted = 0;
    for (int step = 0; step < 1000; ++step) {
        const atm::Cents before = opening + credits - debits;
        const atm::Cents amount = input() % 97;
        const bool credit = input() % 5 < 2;
        const auto result = credit ? account.deposit(amount) : account.withdraw(amount);
        if (amount == 0) {
            CHECK(result == atm::Result::zero_amount);
        } else if (!credit && amount > before) {
            CHECK(result == atm::Result::insufficient_funds);
        } else {
            CHECK(result == atm::Result::ok);
            (credit ? credits : debits) += amount;
            ++accepted;
        }
        CHECK(account.balance() == opening + credits - debits);
        CHECK(account.history().size() == std::min(accepted, atm::Account::history_limit));
        CHECK(account.carried_balance().has_value() == (accepted > atm::Account::history_limit));
        auto running = account.carried_balance().value_or(opening);
        for (const auto& entry : account.history()) {
            if (entry.type == atm::Movement::deposit) running += entry.amount;
            else {
                CHECK(running >= entry.amount);
                running -= entry.amount;
            }
            CHECK(running == entry.balance_after);
        }
        CHECK(running == account.balance());
    }
}
