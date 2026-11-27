#include "session.hpp"

#include "atm/account.hpp"
#include "atm/pin.hpp"

#include <istream>
#include <optional>
#include <ostream>
#include <string>
#include <string_view>

namespace atm {
namespace {

class Terminal {
public:
    Terminal(std::istream& input, std::ostream& output, Account& account)
        : input_(input), output_(output), account_(account) {}

    void run() {
        auto pin = choose_pin();
        if (pin && authenticate(*pin)) show_menu(*pin);
    }

private:
    std::optional<std::string> prompt(std::string_view question) {
        output_ << question << std::flush;
        std::string line;
        if (!std::getline(input_, line)) return std::nullopt;
        const auto first = line.find_first_not_of(" \t\r");
        if (first == line.npos) return std::string{};
        return line.substr(first, line.find_last_not_of(" \t\r") - first + 1);
    }

    std::optional<std::string> choose_pin() {
        output_ << "Local simulation. Use a made-up PIN; input is visible.\n";
        for (;;) {
            auto pin = prompt("Choose a four-digit demo PIN: ");
            if (!pin || valid_pin(*pin)) return pin;
            output_ << "Use exactly four digits (0-9).\n";
        }
    }

    bool authenticate(std::string_view pin) {
        for (int attempt = 0; attempt < 3; ++attempt) {
            const auto entered = prompt("Enter PIN: ");
            if (!entered) return false;
            if (*entered == pin) return true;
            output_ << "Wrong PIN.\n";
        }
        output_ << "Too many attempts. Session ended.\n";
        return false;
    }

    std::optional<std::string> cancellable_prompt(std::string_view question) {
        auto answer = prompt(question);
        if (answer && answer->empty()) {
            output_ << "Cancelled; no changes made.\n";
            return std::nullopt;
        }
        return answer;
    }

    void change_pin(std::string& pin) {
        const auto current = cancellable_prompt("Current PIN (blank to cancel): ");
        if (!current) return;
        if (*current != pin) {
            output_ << "PIN not changed.\n";
            return;
        }
        const auto next = cancellable_prompt("New PIN (blank to cancel): ");
        if (!next) return;
        if (!valid_pin(*next) || *next == pin) {
            output_ << "Choose a different four-digit PIN.\n";
            return;
        }
        const auto confirmation = cancellable_prompt("Repeat new PIN (blank to cancel): ");
        if (!confirmation) return;
        if (*confirmation != *next) {
            output_ << "PIN not changed: confirmation did not match.\n";
            return;
        }
        pin = *next;
        output_ << "Pin changed successfully.\n";
    }

    void show_allowance() {
        if (auto remaining = account_.cash_remaining()) {
            output_ << "Cash allowance left: " << format_amount(*remaining) << '\n';
        }
    }

    void transact(Movement type) {
        const bool debit = type == Movement::withdrawal;
        const auto text = cancellable_prompt(debit ? "Amount to withdraw (blank to cancel): "
                                                  : "Amount to deposit (blank to cancel): ");
        if (!text) return;
        const auto amount = parse_amount(*text);
        if (!amount) {
            output_ << "Enter a positive amount, for example 12.50.\n";
            return;
        }
        const auto result = debit ? account_.withdraw(*amount) : account_.deposit(*amount);
        switch (result) {
            case Result::zero_amount:
                output_ << "Enter a positive amount, for example 12.50.\n";
                return;
            case Result::insufficient_funds:
                output_ << "Insufficient balance.\n";
                return;
            case Result::balance_limit:
                output_ << "Deposit would exceed the balance limit.\n";
                return;
            case Result::cash_limit:
                output_ << "Withdrawal exceeds the remaining cash allowance.\n";
                show_allowance();
                return;
            case Result::ok: break;
        }
        output_ << (debit ? "Withdrawal amount: " : "Deposit amount: ") << format_amount(*amount) << '\n';
        output_ << "Remaining balance: " << format_amount(account_.balance()) << '\n';
        if (debit) show_allowance();
    }

    void show_statement() {
        const auto& history = account_.history();
        if (history.empty()) {
            output_ << "No transactions yet.\n";
            return;
        }
        output_ << "Recent transactions (newest first):\n";
        for (auto row = history.rbegin(); row != history.rend(); ++row) {
            output_ << (row->type == Movement::withdrawal ? "Withdrawal -" : "Deposit +")
                      << format_amount(row->amount) << " | balance "
                      << format_amount(row->balance_after) << '\n';
        }
        if (auto prior = account_.carried_balance()) {
            output_ << "Earlier transactions omitted; balance carried forward: "
                      << format_amount(*prior) << '\n';
        }
    }

    void show_menu(std::string& pin) {
        constexpr std::string_view menu =
            "1) Check balance\n2) Withdraw\n3) Change PIN\n4) Deposit\n"
            "5) Recent transactions\n6) Lock session\n0) Exit\nChoice: ";
        for (;;) {
            const auto choice = prompt(menu);
            if (!choice || *choice == "0") return;
            if (*choice == "1") {
                output_ << "Balance: " << format_amount(account_.balance()) << '\n';
                show_allowance();
            } else if (*choice == "2") transact(Movement::withdrawal);
            else if (*choice == "3") change_pin(pin);
            else if (*choice == "4") transact(Movement::deposit);
            else if (*choice == "5") show_statement();
            else if (*choice == "6") {
                output_ << "Session locked. Sign in to continue.\n";
                if (!authenticate(pin)) return;
            } else output_ << "Invalid choice.\n";
        }
    }

    std::istream& input_;
    std::ostream& output_;
    Account& account_;
};

}  // namespace

void run_session(std::istream& input, std::ostream& output, Account& account) {
    Terminal(input, output, account).run();
}

}  // namespace atm
