#pragma once

#include "atm/money.hpp"

namespace atm {

enum class Result { ok, zero_amount, insufficient_funds };

class Account {
public:
    explicit Account(Cents opening_balance) : balance_(opening_balance) {}

    Cents balance() const { return balance_; }

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
