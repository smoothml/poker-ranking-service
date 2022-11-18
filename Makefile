.DEFAULT_GOAL := help
SHELL := /bin/bash

.PHONY: black
black: ## Run black formatter
	@poetry run black poker tests;

.PHONY: black-check
black-check: ## Run black formatter
	@poetry run black poker tests --check;

.PHONY: clean
clean: ## Remove python cache files
	-@find . -name '*.pyc' -exec rm -f {} +;
	-@find . -name '*.pyo' -exec rm -f {} +;
	-@find . -name '*__pycache__' -exec rm -fr {} +;
	-@find . -name '*.mypy_cache' -exec rm -fr {} +;
	-@find . -name '*.pytest_cache' -exec rm -fr {} +;
	-@find . -name '*.coverage' -exec rm -fr {} +;

.PHONY: coverage
coverage: ## Report test coverage
	@poetry run coverage report --rcfile=setup.cfg;

.PHONY: flake8
flake8: ## Run flake8 linting
	@poetry run flake8 poker tests --config=setup.cfg;

.PHONY: force-update
force-update: ## Forcefully update poetry.lock using pyproject.toml
	-@rm poetry.lock;
	@poetry update;

.PHONY: format
format: isort black ## Format to match linting requirements

.PHONY: help
help: ## Show all available commands
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-13s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST);

.PHONY: install
install: ## Install all packages using poetry.lock
	@poetry install --no-interaction;

.PHONY: install-prod
install-prod: ## Install all production packages using poetry.lock
	@poetry install --no-interaction --only main;

.PHONY: isort
isort: ## Run isort formatter
	@poetry run isort poker tests --settings-path=setup.cfg;

.PHONY: isort-check
isort-check: ## Run isort formatter
	@poetry run isort poker tests --settings-path=setup.cfg --check-only;

.PHONY: mypy
mypy: ## Run mypy type checking
	@poetry run mypy --config-file=setup.cfg poker tests;

.PHONY: pydocstyle
pydocstyle: ## Run docstring linting
	@poetry run pydocstyle poker tests --config=setup.cfg;

.PHONY: quality
quality: flake8 mypy isort-check black-check pydocstyle ## Run linting checks

.PHONY: test
test: ## Run test pipeline
	@poetry run coverage run --rcfile=setup.cfg --source=poker -m pytest -c=setup.cfg -x

.PHONY: uninstall
uninstall: ## Remove virtual environment
	@-rm -rf `poetry env info -p`;

.PHONY: update
update: ## Update poetry.lock using pyproject.toml
	@poetry update;