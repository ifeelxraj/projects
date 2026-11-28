#include "atm/atm_simulator_account.hpp"
#include "atm_simulator_test_checks.hpp"

int main() {
    using atm::Result;
    atm::Account limited(100, 30);
    CHECK(limited.withdraw(20) == Result::ok);
    CHECK(limited.cash_remaining() == 10);
    CHECK(limited.deposit(40) == Result::ok);
    CHECK(limited.withdraw(11) == Result::cash_limit);
    CHECK(limited.withdraw(121) == Result::insufficient_funds);
    CHECK(limited.balance() == 120);
    CHECK(limited.history().size() == 2);
    CHECK(limited.cash_remaining() == 10);
    CHECK(limited.withdraw(10) == Result::ok);
    CHECK(limited.cash_remaining() == 0);
    CHECK(limited.withdraw(1) == Result::cash_limit);

    atm::Account unlimited(100);
    CHECK(!unlimited.cash_remaining());
    CHECK(unlimited.withdraw(100) == Result::ok);
}
