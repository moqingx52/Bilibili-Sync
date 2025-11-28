.PHONY: lint format type test e2e

lint:
	ruff check backend/src backend/tests

format:
	black backend/src backend/tests

type:
	mypy backend/src

test:
	pytest --maxfail=1 --disable-warnings -q

run:
	python -m app

e2e:
	pytest backend/tests/e2e
