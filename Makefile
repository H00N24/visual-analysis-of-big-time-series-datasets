PIP_COMPILE_FLAGS = -U --generate-hashes --build-isolation --allow-unsafe
PYTHON_SOURCES = src setup.py
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
	pip-compile $(PIP_COMPILE_FLAGS) -o requirements.txt setup.py
	pip-compile $(PIP_COMPILE_FLAGS) -o requirements-dev.txt requirements-dev.in

cython-fastdtw:
	cd libs/fastdtw && \
	python setup.py build && \
	python setup.py install

.PHONY: default fmt check black black-check flake8 mypy requirements cython-fastdtw
