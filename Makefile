.ensure-poetry:
	@poetry --version > /dev/null 2>&1 || pip install poetry

setup: poetry.lock pyproject.toml .ensure-poetry
	@poetry install

coverage:
	@poetry run pytest -k 'not test_integration' --cov=apps --cov=src --cov-report=term-missing --cov-report=xml ./tests/

test:
	@poetry run pytest -k 'not test_integration'

test-matching:
	@poetry run pytest -s -rx -k $(Q) src ./tests/

integration-test:
	@poetry run pytest -k "integration"

bandit:
	@poetry run bandit -r -f custom app

mypy:
	@poetry run mypy src/

flake8:
	@poetry run flake8 src/
	@poetry run flake8 tests/ --extend-ignore=ANN

isort-check:
	@poetry run isort -c --profile=black -l 120 .

isort:
	@poetry run isort --profile=black -l 120 .

black:
	@poetry run black . --skip-string-normalization

black-check:
	@poetry run black --skip-string-normalization --check .

lint: isort black

lint-check: mypy flake8 isort-check black-check bandit

build: lint-check test

update: poetry.lock
	@poetry update
