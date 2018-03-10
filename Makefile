CPUS ?= $(shell sysctl -n hw.ncpu || echo 1)
MAKEFLAGS += --jobs=$(CPUS)

reset-db:
	$(MAKE) drop-db
	$(MAKE) create-db

create-db:
	createdb -E utf-8 cuckoo

drop-db:
	dropdb --if-exists cuckoo

test:
	py.test tests
