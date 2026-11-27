#include "atm/account.hpp"
#include "session.hpp"

#include <iostream>

int main() {
    atm::Account account{1'000'000};
    atm::run_session(std::cin, std::cout, account);
}
