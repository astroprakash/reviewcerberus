.PHONY: test lint format

test:
	poetry run pytest -v

lint:
	poetry run mypy src tests
	poetry run isort --check-only src tests
	poetry run black --check src tests

format:
	poetry run isort src tests
	poetry run black src tests
