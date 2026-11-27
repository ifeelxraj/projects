#pragma once

#include <iosfwd>

namespace atm {
class Account;
enum class SessionExit { closed, attempts_exhausted };

// Run one local terminal session; the caller owns the account and streams.
SessionExit run_session(std::istream& input, std::ostream& output, Account& account);
}  // namespace atm
