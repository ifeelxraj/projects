#pragma once

#include "atm/money.hpp"

namespace atm {

enum class Result { ok, zero_amount, insufficient_funds, balance_limit };

class Account {
public:
    explicit Account(Cents opening_balance) : balance_(opening_balance) {}

    Cents balance() const { return balance_; }

    Result deposit(Cents amount) {
        if (amount == 0) return Result::zero_amount;
        if (amount > std::numeric_limits<Cents>::max() - balance_) return Result::balance_limit;
        balance_ += amount;
        return Result::ok;
    }

    Result withdraw(Cents amount) {
        if (amount == 0) return Result::zero_amount;
        if (amount > balance_) return Result::insufficient_funds;
        balance_ -= amount;
        return Result::ok;
    }

private:
    Cents balance_;
};

}  // namespace atm
