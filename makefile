# Makefile — Chess (CLI) — portable Windows/macOS/Linux
# Utilisation : make help

PY ?= python3
PIP ?= $(PY) -m pip
VENV ?= venv

# Exécutables du venv
BIN := $(VENV)/bin
ifeq ($(OS),Windows_NT)
  BIN := $(VENV)/Scripts
endif
PY_VENV := $(BIN)/python
PIP_VENV := $(PY_VENV) -m pip

# Sources
SRC_PATHS := controllers models views constant.py type_validation.py main.py

.PHONY: help
help: ## Affiche cette aide
	@grep -E '^[a-zA-Z0-9._-]+:.*?## ' Makefile | sed 's/:.*##/: /' | column -s': ' -t

# --- Environnement ---"
$(VENV): ## Crée l'environnement virtuel local
	$(PY) -m venv $(VENV)
	$(PIP_VENV) install --upgrade pip wheel

.PHONY: sync
sync: $(VENV) ## Installe les dépendances applicatives
	@if [ -f requirements.txt ]; then \
		echo ">> Installation depuis requirements.txt"; \
		$(PIP_VENV) install -r requirements.txt ; \
	else \
		echo ">> Aucun requirements.txt (ok si projet simple)"; \
	fi

.PHONY: add-dev
add-dev: $(VENV) ## Installe black, flake8, mypy, pytest
	$(PIP_VENV) install -U black flake8 mypy pytest pytest-cov

# --- Qualité ---
.PHONY: format
format: $(VENV) ## Formate avec black
	$(PY_VENV) -m black $(SRC_PATHS)

.PHONY: lint
lint: $(VENV) ## Lint avec flake8
	$(PY_VENV) -m flake8 $(SRC_PATHS) --exclude venv,Data,Doc,__pycache__

.PHONY: typecheck
typecheck: $(VENV) ## Types avec mypy
	$(PY_VENV) -m mypy models || true

# --- Tests (optionnels) ---
.PHONY: test
test: $(VENV) ## Lance pytest si tests/ existe
	@if [ -d tests ]; then $(PY_VENV) -m pytest -q ; else echo "Pas de dossier tests/"; fi

.PHONY: cov
cov: $(VENV) ## Tests + couverture
	@if [ -d tests ]; then \
		$(PY_VENV) -m pytest --cov=models --cov-report=term-missing --cov-report=html ; \
		echo "Rapport HTML : file://$(PWD)/htmlcov/index.html" ; \
	else echo "Pas de dossier tests/"; fi

# --- Exécution ---
.PHONY: run
run: $(VENV) ## Exécute main.py
	$(PY_VENV) main.py

.PHONY: repl
repl: $(VENV) ## Ouvre un REPL dans le venv
	$(PY_VENV)

# --- Nettoyage ---
.PHONY: clean
clean: ## Nettoie caches/artefacts
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov \
	       **/__pycache__ **/*.pyc **/*.pyo

.PHONY: reset
reset: clean ## Supprime aussi le venv
	rm -rf $(VENV)

# --- Pipeline rapide ---
.PHONY: check
check: format lint typecheck test ## Format + lint + types + tests
