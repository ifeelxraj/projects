#pragma once

#include "atm/money.hpp"

#include <cstddef>
#include <deque>
#include <limits>

namespace atm {

enum class Result { ok, zero_amount, insufficient_funds, balance_limit };

enum class Movement { withdrawal, deposit };

struct Transaction {
    Movement type;
    Cents amount;
    Cents balance_after;
};

class Account {
public:
    static constexpr std::size_t history_limit = 10;

    explicit Account(Cents opening_balance) : balance_(opening_balance) {}

    Cents balance() const { return balance_; }
    // Retained entries are in posting order (oldest first).
    const std::deque<Transaction>& history() const { return history_; }

    Result deposit(Cents amount) {
        if (amount == 0) return Result::zero_amount;
        if (amount > std::numeric_limits<Cents>::max() - balance_) return Result::balance_limit;
        return post(Movement::deposit, amount, balance_ + amount);
    }

    Result withdraw(Cents amount) {
        if (amount == 0) return Result::zero_amount;
        if (amount > balance_) return Result::insufficient_funds;
        return post(Movement::withdrawal, amount, balance_ - amount);
    }

private:
    Result post(Movement type, Cents amount, Cents after) {
        history_.push_back({type, amount, after});
        if (history_.size() > history_limit) history_.pop_front();
        balance_ = after;
        return Result::ok;
    }

    Cents balance_;
    std::deque<Transaction> history_;
};

}  // namespace atm
