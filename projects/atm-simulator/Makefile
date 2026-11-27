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

.PHONY: test
test: build/atm
	python3 -m unittest discover -s tests -p 'test_*.py'
