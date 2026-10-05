.PHONY: install lint typecheck test test-unit test-integration test-e2e clean build docs

install:
	pip install -e ".[dev]"

lint:
	ruff check .

typecheck:
	mypy cdpwave/

test: test-unit test-integration

test-unit:
	pytest tests/unit/ -v --cov=cdpwave --cov-report=term-missing

test-integration:
	pytest tests/integration/ -m integration -v

test-e2e:
	pytest tests/e2e/ -m e2e -v

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache .mypy_cache .ruff_cache htmlcov coverage.xml

build:
	python -m build

docs:
	mkdocs serve
