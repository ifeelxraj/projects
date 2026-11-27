# ATM simulator

A local C++ console exercise for checking a balance, making a withdrawal, and
changing a demo PIN. State lives in memory for one run. This is not banking
software and does not connect to a bank, an SMS service, or a payment system.

## Build and try it

From this directory, with GNU Make and a C++17 compiler:

```sh
make
./build/atm
```

The starter demo uses `2486` as its public sample PIN. Choose `1` at the menu
to see the opening balance of 10000. Use fictional inputs only.

Run `make test` with Python 3 installed for end-to-end checks of the compiled
program. The checks do not require any Python packages.
