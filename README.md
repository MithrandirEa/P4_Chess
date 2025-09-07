
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
    make sync
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

### Installation

```bash
pip install flake8 flake8-html
```

### Générer un rapport lint en HTML

```bash
make rapport_lint
```

Cela crée un dossier `flake8_rapport/` contenant `index.html`.

### Ouvrir le rapport automatiquement

```bash
make lintplay
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
│
│── main.py
│── constant.py
│── makefile
```

---

## 🛠 Commandes Makefile utiles

* **Lancer l’app :**

  ```bash
  make run
  ```
* **Vérifier le code (rapport HTML) :**

  ```bash
  make lint
  ```
* **Ouvrir le rapport lint dans le navigateur :**

  ```bash
  make lintplay
  ```

---
