
---

# 📘 README — Gestionnaire de Tournois d’Échecs (CLI)

## 🚀 Prérequis

* **Python 3.9+** installé
* **pip** et **venv** disponibles
* Un terminal (PowerShell, Bash, etc.)

---

## 📦 Installation

1. Clonez ce dépôt et placez-vous dedans :

   ```bash
   git clone https://github.com/MithrandirEa/P4_Chess.git
   cd Chess
   ```

2. Créez, activez un environnement virtuel et installer les dépendances :

   ```bash
    python -m venv venv
    venv\Scripts\Activate
    pip install -r requirements.txt
   ```

---

## ▶️ Lancer l’application

Dans le terminal, exécutez :

```bash
python main.py
```

Vous verrez apparaître le **menu principal** :

```
=== Menu Principal ===
1. Créer un tournoi
2. Gérer un tournoi
3. Afficher les rapports
0. Quitter
```

---

## 📊 Rapports et affichages

### Menu des rapports

* **Joueurs FFE** (liste alphabétique depuis `Data/LicensedPlayers.json`)
* **Tous les tournois** (affiche `Data/Tournaments.json`)
* **Joueurs d’un tournoi** (affiche et trie alphabétiquement les joueurs)
* **Rounds et matchs d’un tournoi** (affiche rounds + matchs avec `tabulate`)

---

## ✅ Vérification de code (Lint)

Nous utilisons **flake8** et **flake8-html**.



### Générer un rapport lint en HTML

```bash
flake8 --max-line-length=119 --format=html --htmldir=flake8_report
```

Cela crée un dossier `flake8_report/` contenant `index.html`.

### Ouvrir le rapport automatiquement

```bash
start flake8_report/index.html   # Windows
xdg-open flake8_report/index.html  # Linux
open flake8_report/index.html     # macOS
```

Cela lancera votre navigateur par défaut et affichera le rapport.

---

## 📂 Structure du projet

```
project/
│── controllers/
│   ├── tournaments_control.py
│   ├── rounds_control.py
│   └── saving_control.py
│
│── models/
│   ├── player.py
│   ├── match.py
│   ├── chessRound.py
│   └── tournament.py
│
│── views/
│   ├── menu.py
│   ├── view_models.py
│   ├── display_round.py
│   └── display_tournament.py
│
│── Data/
│   ├── FakePlayers.json
│   ├── LicensedPlayers.json
│   └── Tournaments.json
│── flake8_report/
│   └── FakePlayers.json
│
│── main.py
│── constant.py
│── type_validation.py
└── requirements.txt
```

