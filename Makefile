.PHONY: test catalog

test: catalog
	$(MAKE) -C projects/atm-simulator test
	$(MAKE) -C projects/csv-cleaner test
	$(MAKE) -C projects/slot-finder test

catalog:
	python3 tools/check_index.py
	python3 -m unittest discover -s tools/tests
