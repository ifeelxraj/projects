.PHONY: test catalog

test: catalog
	$(MAKE) -C projects/atm-simulator test
	$(MAKE) -C projects/csv-cleaner test
	$(MAKE) -C projects/slot-finder test

catalog:
	python3 tools/projects_catalog_check.py
	python3 -m unittest discover -s tools/tests

.PHONY: demo
demo:
	$(MAKE) -C projects/atm-simulator demo
	$(MAKE) -C projects/csv-cleaner demo
	$(MAKE) -C projects/slot-finder demo
	python3 examples/availability/csv_cleaner_to_slot_finder.py

.PHONY: verify
verify: test
	$(MAKE) -C projects/atm-simulator test-ubsan
	$(MAKE) demo
