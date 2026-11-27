#include "atm/account.hpp"
#include "session.hpp"

#include <iostream>
#include <optional>
#include <string_view>

namespace {
constexpr std::string_view usage =
    "Usage: atm [--opening-balance AMOUNT] [--cash-limit AMOUNT]\n"
    "       atm --help\n"
    "Set the initial balance in decimal units (default: 10000.00).\n"
    "Optionally cap total withdrawals for this run (default: no cap).\n";

int usage_error(std::string_view message) {
    std::cerr << "Error: " << message << '\n' << usage;
    return 2;
}
}  // namespace

int main(int argc, char* argv[]) {
    if (argc == 2 && (std::string_view(argv[1]) == "--help" || std::string_view(argv[1]) == "-h")) {
        std::cout << usage;
        return 0;
    }

    std::optional<atm::Cents> opening;
    std::optional<atm::Cents> cash_limit;
    for (int i = 1; i < argc; ++i) {
        const std::string_view option = argv[i];
        if (option != "--opening-balance" && option != "--cash-limit") return usage_error("Unexpected argument.");
        auto& value = option == "--opening-balance" ? opening : cash_limit;
        if (value) return usage_error("Option specified more than once.");
        if (++i == argc) return usage_error("Missing amount after option.");
        value = atm::parse_amount(argv[i]);
        if (!value) return usage_error("Expected a nonnegative decimal amount with at most two fractional digits.");
    }
    atm::Account account{opening.value_or(1'000'000), cash_limit};
    atm::run_session(std::cin, std::cout, account);
}
