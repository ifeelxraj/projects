# ATM simulator

Practice a cash withdrawal, make a deposit, then reconcile both against a
mini-statement. Everything is local to one process: no bank connection, real
money, files of account data, or SMS recovery. **Use a made-up PIN.** Input is
visible as you type; this is a classroom simulation, not an authentication system.

## Where to start reading

Start with the [terminal menu](src/atm_simulator_session.cpp) if you want to see
what a customer can do. Follow a withdrawal into the account file to see why
it succeeds or is declined.

| File | What it does |
| --- | --- |
| [atm_simulator_main.cpp](src/atm_simulator_main.cpp) | Starts the program and sets the opening balance and optional cash limit. |
| [atm_simulator_session.cpp](src/atm_simulator_session.cpp) | Runs sign-in, the menu and the prompts. The [matching header](src/atm_simulator_session.hpp) declares how to start a session. |
| [atm_simulator_account.hpp](include/atm/atm_simulator_account.hpp) | Changes the balance and remembers the last ten successful transactions. |
| [atm_simulator_money.hpp](include/atm/atm_simulator_money.hpp) | Reads and prints amounts in exact cents. |
| [atm_simulator_pin.hpp](include/atm/atm_simulator_pin.hpp) | Checks that a demo PIN has four digits. |
| [atm-simulator-mini-statement.in](examples/atm-simulator-mini-statement.in) | Sample keystrokes for `make demo`, not program code. |

The [tests](tests/) check the feature named after `test_atm_simulator_` in each
filename. You do not need to open them to run the simulator.

## Build and run

You need GNU Make and a C++17 compiler. From the repository root:

```sh
cd projects/atm-simulator
make
./build/atm
```

Choose a four-digit demo PIN, including any leading zeroes, then sign in with
the same PIN. The default opening balance is `10000.00` in fictional units.

```sh
./build/atm --help
./build/atm --opening-balance 25.00 --cash-limit 7.00
```

`--opening-balance` can be zero. `--cash-limit` optionally caps **total** cash
withdrawn in this run, not the size of each withdrawal. Depositing money or
locking and unlocking does not restore that allowance. Omit the option for no cap.

## At the terminal

| Key | Action |
| --- | --- |
| `1` | Check the balance and, if configured, the remaining cash allowance. |
| `2` | Withdraw. Both funds and allowance must cover the amount. |
| `3` | Change PIN. Supply the current PIN and confirm a different four-digit one. |
| `4` | Deposit into the account. |
| `5` | Show up to ten successful movements, newest first, with the balance after each. If older entries were dropped, their closing balance is carried forward. |
| `6` | Lock the terminal. Sign in to the same account without losing its state. |
| `0` | Exit and discard the account, PIN and statement. |

Amounts are integer cents internally. Enter `8`, `8.5`, or `8.50`, **not**
`.50`, `1,000`, a signed value, or a value that needs rounding. The largest
representable balance is `184467440737095516.15`. Deposits and withdrawals must
be positive. A declined action changes neither balances nor history. A blank
line at an amount or change-PIN prompt cancels that action.

EOF exits cleanly, including halfway through an entry. For scripts, exit `0`
means normal exit, help or EOF; `1` means three sign-in attempts failed;
`2` means invalid startup arguments (diagnostic on stderr).

## Replay a session

`make demo` feeds [a sample input stream](examples/atm-simulator-mini-statement.in) to the
binary. It starts at `25.00`, deposits `2.75`, withdraws `5.20`, locks, then
signs back in to display these statement rows:

```text
Withdrawal -5.20 | balance 22.55
Deposit +2.75 | balance 27.75
```

The balance is `22.55`, with `1.80` left of the original `7.00` cash allowance.

## Verify changes

```sh
make test         # C++ unit suites + Python 3 end-to-end tests; no packages needed
make test-ubsan   # same checks with the compiler's undefined-behavior sanitizer
make clean        # remove this project's build/ directory
```
