#include "atm/account.hpp"
#include "session.hpp"

#include <iostream>
#include <optional>
#include <string_view>

namespace {
constexpr std::string_view usage =
    "Usage: atm [--opening-balance AMOUNT]\n"
    "       atm --help\n"
    "Set the initial balance in decimal units (default: 10000.00).\n";

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
    for (int i = 1; i < argc; ++i) {
        if (std::string_view(argv[i]) != "--opening-balance") return usage_error("Unexpected argument.");
        if (opening) return usage_error("Opening balance was specified more than once.");
        if (++i == argc) return usage_error("Missing opening balance.");
        opening = atm::parse_amount(argv[i]);
        if (!opening) return usage_error("Expected a nonnegative decimal amount with at most two fractional digits.");
    }
    atm::Account account{opening.value_or(1'000'000)};
    atm::run_session(std::cin, std::cout, account);
}
