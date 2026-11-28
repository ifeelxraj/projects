# Small projects

There are three programs here. You don't need to read or run them in order.
**Click a project name for its instructions**, or use the code link to see how
that program works.

| Project | What it's for | A good first code file | Status |
| --- | --- | --- | --- |
| [ATM simulator](projects/atm-simulator/) | Use a pretend ATM: deposit money, withdraw it, and see the new balance. No real banking. | [The ATM menu and prompts](projects/atm-simulator/src/atm_simulator_session.cpp) | Complete |
| [CSV cleaner](projects/csv-cleaner/) | Check a spreadsheet saved as CSV, spot bad rows, and write a tidy copy without editing the original. | [How a row gets cleaned](projects/csv-cleaner/csvclean/csv_cleaner_pipeline.py) | Complete |
| [Slot finder](projects/slot-finder/) | Give it working hours and room bookings; it tells you when a meeting will fit. | [How it finds gaps between bookings](projects/slot-finder/slotfind/slot_finder_free_time.py) | Complete |

## See a program in action

From the repository root, pick one demo. The ATM needs GNU Make and a C++17
compiler; the other two demos use Make, a shell and Python 3.9 or later.

```sh
make -C projects/atm-simulator demo   # replay a deposit, a withdrawal and a statement
make -C projects/csv-cleaner demo     # turn three messy stock rows into two clean rows
make -C projects/slot-finder demo     # suggest two meeting times in a shared morning
```

Want to see the Python projects work together? The [booking import example](examples/availability/)
cleans a room-booking table before looking for free time. Its sample produces
30-minute meetings starting at **10:30** and **11:30**.

## How to read the filenames

- **Program code** names the project and the job. For example, `atm_simulator_account.hpp` holds the balance rules, `csv_cleaner_reader.py` reads table rows, and `slot_finder_time_ranges.py` handles start and end times. Each project's README has a short file-by-file guide.
- **`test_…` means an automated check**, not another app. For example, `test_csv_cleaner_sort_order.py` checks the CSV cleaner's sorting rule. **`examples/`** contains sample data and demos.
- **`README.md`** is the guide GitHub opens when you visit a folder. **`Makefile`** contains shortcuts like `make demo`. Python's **`__init__.py`** and **`__main__.py`** keep their standard names so the packages and `python3 -m` commands still work.

**For maintainers:** [`tools/`](tools/) checks the project list and prepares the daily brief;
[`.github/workflows/`](.github/workflows/) runs checks on GitHub. Neither is another project.
Run `make test` to check the repository or `python3 tools/projects_daily_brief.py` to read the
latest [work log](logs/). The [contributor guide](CONTRIBUTING.md) covers the workflow.
