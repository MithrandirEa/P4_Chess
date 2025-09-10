# Nom du venv
VENV := venv
PYTHON = venv\Scripts\python
PIP := venv/Scripts/pip

# Répertoires du projet
SRC_PATHS := chessManager/controllers chessManager/models chessManager/views main.py constant.py type_validation.py

# =====================================================================
# Commandes principales
# =====================================================================

.PHONY: help
help:  ## Affiche cette aide
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# =====================================================================
# Environnement
# =====================================================================

$(VENV): ## Crée l'environnement virtuel
	python -m venv $(VENV)
	$(PYTHON) -m pip install --upgrade pip wheel

.PHONY: sync
sync: $(VENV) ## Installe les dépendances dans le venv
ifeq (,$(wildcard requirements.txt))
	@echo ">> Aucun requirements.txt (ok si projet simple)"
else
	$(PIP) install -r requirements.txt
endif

.PHONY: add-dev
add-dev: $(VENV) ## Installe black, flake8, mypy, pytest et flake8-html
	$(PIP) install -U black flake8 flake8-html mypy pytest pytest-cov

# =====================================================================
# Qualité du code
# =====================================================================

.PHONY: format
format: $(VENV) ## Formate avec black
	$(PYTHON) -m black $(SRC_PATHS)

.PHONY: lint
lint: $(VENV) ## Analyse du code avec flake8
	$(PYTHON) -m flake8 --max-line-length=119 $(SRC_PATHS) --exclude venv,__pycache__,Data,test

.PHONY: lint-html
lint-html: $(VENV) ## Génère un rapport HTML flake8
	$(PYTHON) -m flake8 --max-line-length=119 --format=html --htmldir=flake8_report $(SRC_PATHS) --exclude venv,__pycache__,Data,test || exit 0

.PHONY: lint-play
lint-play: lint-html ## Ouvre le rapport HTML flake8
	powershell -Command "Start-Process flake8_report/index.html"




# =====================================================================
# Lancement du projet
# =====================================================================

.PHONY: run
run: $(VENV) ## Exécute le programme principal
	$(PYTHON) main.py

# =====================================================================
# Nettoyage
# =====================================================================

.PHONY: clean
clean: ## Supprime venv, caches et rapports
	@if exist $(VENV) rmdir /s /q $(VENV)
	@if exist __pycache__ rmdir /s /q __pycache__
	@if exist flake8_report rmdir /s /q flake8_report
	@for /d %%d in (controllers\__pycache__ models\__pycache__ views\__pycache__) do if exist %%d rmdir /s /q %%d
	@echo ">> Nettoyage terminé."
