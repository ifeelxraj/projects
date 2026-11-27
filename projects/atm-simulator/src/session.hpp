#pragma once

#include <iosfwd>

namespace atm {
class Account;

// Run one local terminal session; the caller owns the account and streams.
void run_session(std::istream& input, std::ostream& output, Account& account);
}  // namespace atm
