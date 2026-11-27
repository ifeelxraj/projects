#include "atm/money.hpp"
#include "check.hpp"

int main() {
    using atm::format_amount;
    using atm::parse_amount;
    CHECK(format_amount(0) == "0.00");
    CHECK(format_amount(9) == "0.09");
    CHECK(format_amount(210) == "2.10");
    const auto largest = std::numeric_limits<atm::Cents>::max();
    CHECK(format_amount(largest) == "184467440737095516.15");
    CHECK(parse_amount(format_amount(largest)) == largest);
    CHECK(parse_amount("0") == 0);
    CHECK(parse_amount("17") == 1700);
    CHECK(parse_amount("0003.5") == 350);
    CHECK(parse_amount("0.09") == 9);
    // Both the fractional digit and the implicit trailing zero can overflow.
    CHECK(parse_amount("184467440737095516.15") == std::numeric_limits<atm::Cents>::max());
    CHECK(!parse_amount("184467440737095516.16"));
    CHECK(!parse_amount("184467440737095517"));
    CHECK(!parse_amount("999999999999999999999999999"));

    for (auto invalid : {"", ".5", "2.", "2.345", "+2", "-0.5", "2e1", "1,000",
                         "1..0", "12xyz", " 3", "3 "}) {
        CHECK(!parse_amount(invalid));
    }
}
