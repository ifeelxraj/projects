#pragma once

#include "atm/atm_simulator_money.hpp"

#include <cstddef>
#include <deque>
#include <limits>
#include <optional>

namespace atm {

enum class Result { ok, zero_amount, insufficient_funds, balance_limit, cash_limit };

enum class Movement { withdrawal, deposit };

struct Transaction {
    Movement type;
    Cents amount;
    Cents balance_after;
};

class Account {
public:
    static constexpr std::size_t history_limit = 10;

    explicit Account(Cents opening_balance, std::optional<Cents> cash_limit = std::nullopt)
        : balance_(opening_balance), cash_remaining_(cash_limit) {}

    Cents balance() const { return balance_; }
    std::optional<Cents> cash_remaining() const { return cash_remaining_; }
    // Retained entries are in posting order (oldest first).
    const std::deque<Transaction>& history() const { return history_; }

    // Set only after eviction: the balance immediately before the first retained entry.
    std::optional<Cents> carried_balance() const { return carried_balance_; }

    Result deposit(Cents amount) {
        if (amount == 0) return Result::zero_amount;
        if (amount > std::numeric_limits<Cents>::max() - balance_) return Result::balance_limit;
        post(Movement::deposit, amount, balance_ + amount);
        return Result::ok;
    }

    Result withdraw(Cents amount) {
        if (amount == 0) return Result::zero_amount;
        if (amount > balance_) return Result::insufficient_funds;
        if (cash_remaining_ && amount > *cash_remaining_) return Result::cash_limit;
        post(Movement::withdrawal, amount, balance_ - amount);
        if (cash_remaining_) *cash_remaining_ -= amount;
        return Result::ok;
    }

private:
    void post(Movement type, Cents amount, Cents after) {
        history_.push_back({type, amount, after});
        if (history_.size() > history_limit) {
            carried_balance_ = history_.front().balance_after;
            history_.pop_front();
        }
        balance_ = after;
    }

    Cents balance_;
    std::optional<Cents> cash_remaining_;
    std::deque<Transaction> history_;
    std::optional<Cents> carried_balance_;
};

}  // namespace atm
