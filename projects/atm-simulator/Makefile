CXXFLAGS ?= -O2 -Wall -Wextra -Wpedantic
SOURCES := $(wildcard src/*.cpp)
HEADERS := $(wildcard include/atm/*.hpp src/*.hpp)

ifeq ($(SANITIZE),1)
BUILD := build/ubsan
CHECK_FLAGS := -O1 -g -fsanitize=undefined -fno-sanitize-recover=undefined
else
BUILD := build
endif

.PHONY: all run clean test test-ubsan
all: $(BUILD)/atm

$(BUILD)/atm: $(SOURCES) $(HEADERS) Makefile | $(BUILD)
	$(CXX) $(CPPFLAGS) -Iinclude $(CXXFLAGS) $(CHECK_FLAGS) -std=c++17 $(SOURCES) $(LDFLAGS) -o $@

$(BUILD):
	mkdir -p $@

run: $(BUILD)/atm
	./$(BUILD)/atm

clean:
	$(RM) -r build

UNIT_SOURCES := $(wildcard tests/test_*.cpp)
UNIT_BINS := $(patsubst tests/%.cpp,$(BUILD)/%,$(UNIT_SOURCES))

$(BUILD)/%: tests/%.cpp tests/atm_simulator_test_checks.hpp $(HEADERS) Makefile | $(BUILD)
	$(CXX) $(CPPFLAGS) -Iinclude $(CXXFLAGS) $(CHECK_FLAGS) -std=c++17 $< $(LDFLAGS) -o $@

test: $(BUILD)/atm $(UNIT_BINS)
	@set -e; for suite in $(UNIT_BINS); do echo "[test] $$suite"; ./$$suite; done
	ATM_BINARY="$(abspath $(BUILD)/atm)" python3 -m unittest discover -s tests -p 'test_*.py'

test-ubsan:
	$(MAKE) SANITIZE=1 test

.PHONY: demo
demo: $(BUILD)/atm
	./$(BUILD)/atm --opening-balance 25.00 --cash-limit 7.00 < examples/atm-simulator-mini-statement.in
