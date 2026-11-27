#include "atm/account.hpp"
#include "check.hpp"

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
}
