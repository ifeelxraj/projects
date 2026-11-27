#include "atm/money.hpp"
#include "check.hpp"

int main() {
    using atm::parse_amount;
    CHECK(parse_amount("0") == 0);
    CHECK(parse_amount("17") == 1700);
    CHECK(parse_amount("0003.5") == 350);
    CHECK(parse_amount("0.09") == 9);
    CHECK(!parse_amount(""));
    CHECK(!parse_amount("2.345"));
}
