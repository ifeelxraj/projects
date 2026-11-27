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

At startup, choose a made-up four-digit PIN, then enter it again to sign in.
Leading zeroes count. The terminal does not mask your input, so **never enter
a real PIN**. Choose `1` to see the opening balance of `10000.00`.

Run `make test` with Python 3 installed for end-to-end checks of the compiled
program. The checks do not require any Python packages.
