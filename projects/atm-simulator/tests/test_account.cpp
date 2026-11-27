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
}
