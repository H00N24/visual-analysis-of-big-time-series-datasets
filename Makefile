PYTHON_SOURCES = src
PACKAGE_NAME = feature_dtw

default: check

check: black-check isort-check flake8 mypy

fmt: isort black

black:
	black $(PYTHON_SOURCES)

black-check:
	black --check --diff $(PYTHON_SOURCES)

flake8:
	flake8 $(PYTHON_SOURCES)

isort:
	isort $(PYTHON_SOURCES)

isort-check:
	isort --check --diff $(PYTHON_SOURCES)

mypy:
	mypy $(PYTHON_SOURCES)

requirements:
	@echo "# Please seat back and relax, this may take some time. :)"
	poetry update
	poetry export -f requirements.txt -o requirements.txt
	poetry export --dev -f requirements.txt -o requirements-dev.txt

.PHONY: default fmt check black black-check flake8 mypy requirements cython-fastdtw
