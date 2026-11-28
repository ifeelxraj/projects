#pragma once

#include <string_view>

namespace atm {

// A string preserves leading zeroes and avoids locale-dependent digit rules.
constexpr bool valid_pin(std::string_view text) {
    if (text.size() != 4) return false;
    for (char c : text) {
        if (c < '0' || c > '9') return false;
    }
    return true;
}

}  // namespace atm
