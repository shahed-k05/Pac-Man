.PHONY: install run clean venv lint debug
VENV = .venv
PYTHON = $(VENV)/bin/python3
WHEEL = mazegenerator-2.1.0-py3-none-any.whl

run:
	$(PYTHON) pac-man.py config.json

debug:
	$(PYTHON) -m pdb pac-man.py config.json

venv:
	python3 -m venv $(VENV)

install: $(VENV)/bin/activate
	${PYTHON} -m pip install -U pip
	${PYTHON} -m pip install -r requirements.txt
	${PYTHON} -m pip install ./$(WHEEL)
package:
	pyinstaller pacman.spec
lint:
	flake8 . --exclude=$(VENV)
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs --exclude '(^|/)\$(VENV)/'
clean:
	find . -type d \( -name "__pycache__" -o -name ".mypy_cache" -o -name ".pytest_cache" \) -exec rm -rf {} +
	@find . -type f -name "*.Identifier" -delete
