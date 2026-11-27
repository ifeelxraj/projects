#include "atm/account.hpp"
#include "check.hpp"

int main() {
    using atm::Result;
    atm::Account account(250);
    CHECK(account.balance() == 250);
    CHECK(account.withdraw(251) == Result::insufficient_funds);
    CHECK(account.withdraw(0) == Result::zero_amount);
    CHECK(account.balance() == 250);
    CHECK(account.withdraw(1) == Result::ok);
    CHECK(account.balance() == 249);
    CHECK(account.withdraw(249) == Result::ok);
    CHECK(account.balance() == 0);
    CHECK(account.withdraw(1) == Result::insufficient_funds);

    const auto limit = std::numeric_limits<atm::Cents>::max();
    atm::Account near_limit(limit - 2);
    CHECK(near_limit.deposit(0) == Result::zero_amount);
    CHECK(near_limit.deposit(3) == Result::balance_limit);
    CHECK(near_limit.balance() == limit - 2);
    CHECK(near_limit.deposit(2) == Result::ok);
    CHECK(near_limit.balance() == limit);
    CHECK(near_limit.deposit(1) == Result::balance_limit);
    CHECK(near_limit.balance() == limit);
}
