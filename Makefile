.PHONY: test catalog

test: catalog
	$(MAKE) -C projects/atm-simulator test
	$(MAKE) -C projects/csv-cleaner test
	$(MAKE) -C projects/slot-finder test

catalog:
	python3 tools/check_index.py
	python3 -m unittest discover -s tools/tests

.PHONY: demo
demo:
	$(MAKE) -C projects/atm-simulator demo
	$(MAKE) -C projects/csv-cleaner demo
	$(MAKE) -C projects/slot-finder demo
	python3 examples/availability/plan_export.py
