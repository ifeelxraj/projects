CXXFLAGS ?= -O2 -Wall -Wextra -Wpedantic
SOURCES := $(wildcard src/*.cpp)
HEADERS := $(wildcard include/atm/*.hpp src/*.hpp)

.PHONY: all run clean
all: build/atm

build/atm: $(SOURCES) $(HEADERS) | build
	$(CXX) $(CPPFLAGS) -Iinclude $(CXXFLAGS) -std=c++17 $(SOURCES) $(LDFLAGS) -o $@

build:
	mkdir -p $@

run: build/atm
	./build/atm

clean:
	$(RM) -r build

UNIT_SOURCES := $(wildcard tests/test_*.cpp)
UNIT_BINS := $(patsubst tests/%.cpp,build/%,$(UNIT_SOURCES))

build/%: tests/%.cpp tests/check.hpp $(HEADERS) | build
	$(CXX) $(CPPFLAGS) -Iinclude $(CXXFLAGS) -std=c++17 $< $(LDFLAGS) -o $@

.PHONY: test
test: build/atm $(UNIT_BINS)
	@set -e; for suite in $(UNIT_BINS); do echo "[test] $$suite"; ./$$suite; done
	python3 -m unittest discover -s tests -p 'test_*.py'
