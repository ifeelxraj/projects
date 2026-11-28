#pragma once

#include <cstdlib>
#include <iostream>

// Unlike assert, test checks still run in builds that define NDEBUG.
inline void check(bool ok, const char* expression, const char* file, int line) {
    if (!ok) {
        std::cerr << file << ':' << line << ": failed: " << expression << '\n';
        std::exit(EXIT_FAILURE);
    }
}
#define CHECK(expression) check(static_cast<bool>(expression), #expression, __FILE__, __LINE__)
