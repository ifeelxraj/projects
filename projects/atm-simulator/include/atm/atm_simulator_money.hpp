#pragma once

#include <cstdint>
#include <limits>
#include <optional>
#include <string>
#include <string_view>

namespace atm {

using Cents = std::uint64_t;

// Accept digits with an optional one- or two-digit fraction. Accumulate
// directly in cents: never round, parse a numeric prefix, or wrap on overflow.
inline std::optional<Cents> parse_amount(std::string_view text) {
    const auto dot = text.find('.');
    const auto whole = text.substr(0, dot);
    const auto fraction = dot == text.npos ? std::string_view{} : text.substr(dot + 1);
    if (whole.empty() || (dot != text.npos && (fraction.empty() || fraction.size() > 2))) {
        return std::nullopt;
    }

    Cents value = 0;
    auto append_digit = [&value](char c) {
        if (c < '0' || c > '9') return false;
        const auto digit = static_cast<Cents>(c - '0');
        if (value > (std::numeric_limits<Cents>::max() - digit) / 10) return false;
        value = value * 10 + digit;
        return true;
    };
    for (char c : whole) if (!append_digit(c)) return std::nullopt;
    for (char c : fraction) if (!append_digit(c)) return std::nullopt;
    for (auto i = fraction.size(); i < 2; ++i) {
        if (!append_digit('0')) return std::nullopt;
    }
    return value;
}

inline std::string format_amount(Cents cents) {
    const auto fraction = cents % 100;
    return std::to_string(cents / 100) + (fraction < 10 ? ".0" : ".") + std::to_string(fraction);
}

}  // namespace atm
