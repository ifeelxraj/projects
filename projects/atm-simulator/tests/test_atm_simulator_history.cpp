#include "atm/atm_simulator_account.hpp"
#include "atm_simulator_test_checks.hpp"

int main() {
    using atm::Movement;
    using atm::Result;
    atm::Account account(1000);
    CHECK(account.history().empty());
    CHECK(account.deposit(40) == Result::ok);
    CHECK(account.withdraw(1041) == Result::insufficient_funds);
    CHECK(account.withdraw(6) == Result::ok);
    const auto& log = account.history();
    CHECK(log.size() == 2);
    CHECK(log.front().type == Movement::deposit);
    CHECK(log.front().amount == 40);
    CHECK(log.front().balance_after == 1040);
    CHECK(log.back().type == Movement::withdrawal);
    CHECK(log.back().amount == 6);
    CHECK(log.back().balance_after == account.balance());

    atm::Account full(100);
    for (std::size_t i = 0; i < atm::Account::history_limit + 3; ++i) {
        CHECK(full.deposit(1) == Result::ok);
        CHECK(full.history().size() <= atm::Account::history_limit);
    }
    // None of these may displace even the oldest retained receipt.
    CHECK(full.withdraw(full.balance() + 1) == Result::insufficient_funds);
    CHECK(full.deposit(std::numeric_limits<atm::Cents>::max()) == Result::balance_limit);
    CHECK(full.deposit(0) == Result::zero_amount);
    CHECK(full.history().size() == atm::Account::history_limit);
    atm::Cents expected = 104;
    for (const auto& receipt : full.history()) {
        CHECK(receipt.balance_after == expected++);
    }
    CHECK(full.history().back().balance_after == full.balance());
}
