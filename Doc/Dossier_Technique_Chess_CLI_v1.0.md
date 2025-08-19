# Dossier technique — Application CLI de gestion de tournoi d’échecs (pattern MVC)

**Auteur :** ChatGPT — dossier prêt à importer dans Google Docs  
**Date :** 19 août 2025 (Europe/Paris)

---

## 1) Résumé exécutif

Cette application organise des informations d’un tournoi d’échecs via une interface en ligne de commande (CLI) en respectant le pattern **MVC (Model–View–Controller)** :
- **Model** — Entités métier (`Player`, `Match`, `Round`) et persistance **JSON** (fichier `stores.py`) avec **écriture atomique** pour éviter les corruptions en cas d’interruption.
- **View** — Prompts/affichages (fichier `View.py`) *sans* logique métier.
- **Controller** — Orchestrateur (fichier `Control.py`) qui enchaîne les écrans et appelle l’API du modèle.

Le stockage repose sur deux fichiers JSON : un pour les **joueurs** et un pour les **tours & matches**. L’application garantit des validations minimales (unicité d’ID joueur, résultats de match autorisés, vérification d’existence des joueurs lors de la création d’un match).


## 2) Arborescence et modules

```
project_root/
├─ Control.py                    # Contrôleur (point d’entrée CLI)
├─ View.py                       # Vue (IHM CLI)
├─ constant.py                   # Constantes de configuration
├─ models/
│  ├─ __init__.py                # Ré-export (API package) — À bien nommer avec 2 underscores
│  ├─ player.py                  # Entité Player
│  ├─ match.py                   # Entité Match
│  ├─ round.py                   # Entité Round (contient une liste de Match)
│  └─ stores.py                  # Persistance JSON + services métier
└─ Data/
   ├─ FakePlayers.json           # Créé/normalisé à la volée
   └─ Rounds.json                # Créé/normalisé à la volée
```

> **/attention** : le fichier vu dans les sources s’appelle `__init_.py` (un seul underscore avant `.py`). Il faut le renommer en **`__init__.py`** pour que Python reconnaisse bien `models` comme un package et autorise `from models import ...`.

**Imports internes clés :**
- `Control.py` importe : `View` (vue) et l’API du modèle exposée par `models` (`Player`, `Round`, `Match`, + fonctions store).
- `stores.py` importe les entités `Player`, `Match`, `Round` et les constantes définies dans `constant.py`.


## 3) Bibliothèques & modules utilisés (choix & fonctionnement)

**Standard library uniquement** — robustesse, portabilité, zéro dépendance externe :
- `dataclasses` : crée des entités immuables/légères avec peu de code.  
  - Fournit `@dataclass`, `field(default_factory=...)` pour générer automatiquement des identifiants (`uuid4`) ou des listes vides.
- `typing` : annotations de types (`Dict`, `List`, `Optional`, `TYPE_CHECKING`) — améliore la lisibilité et permet l’analyse statique (mypy/pyright).
- `pathlib.Path` : manipulations de chemins agnostiques (Windows/Linux/Mac), plus sûres que des strings, ex. `Path("Data") / "Rounds.json"`.
- `json` : sérialisation/désérialisation des données vers fichiers JSON.
- `os` : appels système, utilisés notamment pour le **flush + fsync** et le **replace** lors de l’écriture atomique.
- `uuid` : génération d’identifiants uniques (`uuid4`) pour `match_id` et `round_id`.
- `__future__` / `annotations` : différer la résolution des annotations pour éviter les import cycles during typing.
- `if TYPE_CHECKING` : permet d’importer des types **uniquement** pour la complétion/type-checking sans créer de dépendance d’exécution circulaire dans `View.py`.

**Pourquoi ce choix ?**
- **Simplicité & maintenabilité** : tout repose sur la stdlib, pas de verrouillage de version de dépendances.
- **Testabilité** : dataclasses pures + sérialisation déterministe → tests unitaires faciles.
- **Fiabilité** : écriture **atomique** assure la robustesse du stockage même en cas d’arrêt brutal.


## 4) `constant.py` — Configuration centralisée

- `DB_PLAYERS` : `Path("Data") / "FakePlayers.json"` — base joueurs.
- `DB_ROUNDS` : `Path("Data") / "Rounds.json"` — base tours+matches.
- `DEFAULT_ENCODING = "utf-8"` : encodage de lecture/écriture des fichiers.
- `VALID_RESULTS = {"1-0", "0-1", "1/2-1/2", None}` : domaine des résultats autorisés pour un match.

**Raison d’être :** centraliser ces paramètres évite les *magic strings* et facilite une future factorisation (ex. passer à SQLite).


## 5) Entités (Model)

### 5.1 `player.py` — `Player`
```python
@dataclass
class Player:
    name: str
    birthdate: str
    national_chess_id: str
    address: Optional[str] = None
```
- **Invariants métiers (recommandés)** :
  - `name` non vide ; `national_chess_id` non vide et unique.
  - `birthdate` format ISO `YYYY-MM-DD` (à valider côté Vue/Contrôleur ou via utilitaire).
- **Sérialisation** : `to_record()` produit un `dict` JSON-ready ; `from_record()` reconstruit l’objet en tolérant des clés manquantes (valeurs par défaut vides).

**Décision** : l’entité reste *pure* (pas d’I/O, pas de prints).


### 5.2 `match.py` — `Match`
```python
@dataclass
class Match:
    white_id: str
    black_id: str
    board: Optional[int] = None
    result: Optional[str] = None   # "1-0" | "0-1" | "1/2-1/2" | None
    match_id: str = field(default_factory=lambda: str(uuid.uuid4()))
```
- `white_id` et `black_id` référencent `Player.national_chess_id`.  
- `board` : numéro de table (optionnel).  
- `result` : restreint à `VALID_RESULTS` (validation faite côté store).  
- `match_id` : identifiant stable pour mise à jour ultérieure.

**Sérialisation** : `to_record()` / `from_record()` — tolère des enregistrements JSON sans `match_id` (régénère un UUID).


### 5.3 `round.py` — `Round`
```python
@dataclass
class Round:
    name: str
    number: Optional[int] = None
    date: Optional[str] = None
    matches: List[Match] = field(default_factory=list)
    round_id: str = field(default_factory=lambda: str(uuid.uuid4()))
```
- Un **tour** *possède* ses `Match`.  
- **Sérialisation** : inclut la sérialisation de chaque `Match`.  
- `from_record()` reconstruit tout l’objet (y compris sa liste `matches`).

**Conséquence de conception** : les matches sont toujours **rattachés** à l’instance du tour — ce que tu souhaitais.


## 6) Persistance & services (Model) — `stores.py`

### 6.1 Principes
- **Normalisation** : à la lecture, le store convertit des formats “anciens” (liste brute) en format “canonique” (`{"players":[...],"count":N}` / `{"rounds":[...],"count":M}`) et complète les champs manquants (`match_id`, `round_id`).
- **Écriture atomique** :
  1. Écrire dans un fichier **temporaire** (même dossier) ;
  2. `flush()` + `os.fsync(fd)` pour forcer l’écriture disque ;
  3. `os.replace(tmp, cible)` qui est **atomique** sur la plupart des FS → jamais de JSON partiellement écrit.

> Limite : cela ne gère pas la **concurrence multi-processus**. Si plusieurs processus écrivent en même temps, un verrouillage (file lock) serait à ajouter (ex. `fcntl`/`msvcrt` selon OS).

### 6.2 API “players”
- `list_players() -> List[Player]` : retourne toutes les entités désérialisées.
- `add_player(player: Player) -> bool` :
  - **Refuse** les doublons de `national_chess_id` (unicité logique).
  - Met à jour la liste et `count`, puis écrit (atomique).
  - Renvoie `True` si ajouté, `False` sinon.

### 6.3 API “rounds & matches”
- `list_rounds() -> List[Round]` : renvoie tous les tours, désérialisés avec leurs matches.
- `create_round(name: str, number?: int, date?: str) -> Round` : crée un tour vide et le persiste.
- `add_match_to_round(round_id: str, white_id: str, black_id: str, board?: int) -> Optional[Match]` :
  - Valide que `white_id` et `black_id` existent **dans la base joueurs** ;
  - Valide que `white_id != black_id` ;
  - Ajoute le match et persiste. `None` si validation échoue.
- `set_match_result(round_id: str, match_id: str, result: Optional[str]) -> bool` :
  - Valide que `result ∈ VALID_RESULTS` ;
  - Met à jour **le match ciblé** dans le tour ciblé ; persiste ; renvoie `True/False`.
- `list_matches_for_round(round_id: str) -> List[Match]` : aide à afficher/choisir un match côté Vue/Contrôleur.

### 6.4 Formats JSON (schémas d’exemple)

**Joueurs (`FakePlayers.json`)**
```json
{
  "players": [
    {
      "name": "Jane Doe",
      "birthdate": "1990-05-01",
      "national_chess_id": "FR-ABCDE123",
      "address": "12 rue des Échecs, 75000 Paris"
    }
  ],
  "count": 1
}
```

**Tours & matches (`Rounds.json`)**
```json
{
  "rounds": [
    {
      "round_id": "0c2cc7e0-...",
      "name": "Ronde 1",
      "number": 1,
      "date": "2025-08-19",
      "matches": [
        {
          "match_id": "4a7b...",
          "white_id": "FR-ABCDE123",
          "black_id": "FR-ZYX98765",
          "board": 3,
          "result": "1/2-1/2"
        }
      ]
    }
  ],
  "count": 1
}
```


## 7) Vue (IHM CLI) — `View.py`

**Responsabilités :**
- Saisir des données et **afficher** des listes / retours d’opérations ;
- **Aucune** logique métier (pas d’accès direct aux JSON, pas de validation “métier” avancée).

**Techniques notables :**
- `if TYPE_CHECKING:` pour déclarer les types utilisés uniquement par les outils de typage sans import au runtime (évite des dépendances circulaires inutiles).

**Prompts principaux :**
- `ask_yes_no(message: str) -> bool` : normalise `y/o/yes/oui` → `True`.
- `prompt_player_fields() -> Dict[str, str]` : saisit `name`, `birthdate`, `national_chess_id`, `address?`.
- `prompt_round_fields() -> Dict[str, Any]` : saisit `name`, `number?` (cast en `int`), `date?` (string ISO).
- `prompt_match_fields() -> Dict[str, Any]` : saisit `white_id`, `black_id`, `board?` (cast en `int`).

**Affichages usuels :**
- `show_players(players: List[Player])` : liste formatée des joueurs ;
- `show_rounds(rounds: List[Round])` : *tours* + *matches* avec `match_id`, table et résultat ;
- `show_player_added(ok: bool)` / `show_round_created(round: Round)` / `show_match_added(match: Optional[Match])` / `show_set_result(ok: bool)`.

**Améliorations (UX) suggérées :**
- Ajouter une validation de date (`YYYY-MM-DD`) et un re-prompt si invalide.
- Dans le flux résultat, proposer un **sélecteur** de match (index) plutôt que la saisie libre d’un `match_id`.


## 8) Contrôleur — `Control.py`

**Rôle :** enchaîner les flux IHM et appeler les services du modèle.

**Flux “Joueurs” — `flow_players()`**
1. Afficher la liste actuelle (`list_players` + `show_players`).
2. Demander si on veut créer un joueur (`ask_yes_no`).
3. S’il y a création : saisir (`prompt_player_fields`) → construire objet `Player` → `add_player` → feedback (`show_player_added`).
4. Ré-afficher la liste.

**Flux “Tours & matches” — `flow_rounds()`**
1. `Créer un tour` : `prompt_round_fields` → `create_round` → `show_round_created`.
2. `Ajouter un match` : `select_round` → `prompt_match_fields` → `add_match_to_round` → `show_match_added`.
3. `Saisir un résultat` : `select_round` → `show_rounds` (pour voir les `match_id`) → demander `match_id` + `result` → `set_match_result`.
4. `Afficher l’état` : `show_rounds(list_rounds())`.

**Point d’entrée — `main_cli()`**
- Menu simple “1) Gérer les joueurs / 2) Gérer les tours & matches”, puis `flow_players()` ou `flow_rounds()` selon le choix.


## 9) Scénarios pas à pas (E2E)

### 9.1 Ajouter un joueur
- **Vue** : saisie des champs → **Contrôleur** : construit `Player` → **Model** : `add_player` (vérifie doublon, persiste).  
- **Vue** : feedback + liste à jour.

### 9.2 Créer un tour puis y ajouter un match
- **Vue** : saisie tour → **Contrôleur** : `create_round` → **Model** : persiste.  
- **Vue** : sélection du tour, saisie `white_id/black_id` → **Contrôleur** : `add_match_to_round` → **Model** : vérifie existence joueurs, IDs distincts, persiste.  
- **Vue** : feedback + affichage du match (avec `match_id`).

### 9.3 Saisir le résultat d’un match
- **Vue** : sélection du tour + affichage des matches (récupère `match_id`).  
- **Contrôleur** : `set_match_result(round_id, match_id, "1-0" | "0-1" | "1/2-1/2" | None)` → **Model** : validation + persistance.


## 10) Robustesse, erreurs & limites

- **Écriture atomique** : supprime les corruptions “mi-écrit / mi-JSON” en cas de crash.  
- **Normalisation à la lecture** : tolère des formats historiques hétérogènes.  
- **Validations** : existence des joueurs, résultats autorisés, IDs joueurs distincts.  
- **Encodage** : `utf-8` partout.

**Limites et contre-mesures :**
- **Concurrence** (multi-process) : ajouter un verrou fichier (advisory lock) si plusieurs processus peuvent écrire en parallèle.  
- **Intégrité référentielle** : `white_id`/`black_id` ne sont pas des foreign keys “fortes” (JSON). Un passage à SQLite/PostgreSQL renforcerait ceci.  
- **Backups** : prévoir une rotation (ex. conserver `Rounds.json.bakN`).


## 11) Tests (plan recommandé)

**Unitaires (pytest) :**
- `stores.add_player` : ajout OK / doublon refusé.  
- `stores.add_match_to_round` : joueurs manquants, même ID des deux côtés, round introuvable.  
- `stores.set_match_result` : valeurs hors domaine.  
- `stores._read_*` : normalisation (régénération d’UUID manquants).  

**Techniques :**
- Utiliser `tempfile.TemporaryDirectory()` + redirection de `DB_PLAYERS/DB_ROUNDS` (via monkeypatch) pour des tests isolés.  
- Capturer l’I/O de la **Vue** avec `capsys` et simuler `input()` (monkeypatch) pour des tests de flux CLI.

**Property-based (hypothesis)** :  
- Générer des `Player`/`Match` aléatoires et vérifier les invariants (unicité ID joueur ; `white_id != black_id`).


## 12) Exécution & packaging

**Lancer en dev :**
```bash
python Control.py
```

**Préparer un binaire (optionnel) :**
- `pyinstaller --onefile Control.py` (prévoir un `entry_point` clair).  
- S’assurer que le dossier `Data/` est créé si absent.

**Pré-commit qualité (optionnel) :**
- Linter `ruff` ou `flake8`, formatteur `black`, type-checker `mypy/pyright`.


## 13) Roadmap d’évolutions

- **UX CLI** : listes paginées, sélection par index.  
- **Fonctionnel** : calcul de classement, gestion de tournoi (Système Suisse), bye, forfaits.  
- **Persistance** : migration vers SQLite (verrous, requêtes, intégrité référentielle), puis éventuellement PostgreSQL.  
- **I18N** : messages en anglais/français via table de traductions.  
- **Journalisation** : `logging` avec niveaux (INFO/WARN/ERROR) + fichier de log.  
- **Sécurité & RGPD** : chiffrer `address`, politique de rétention, droits d’accès.


## 14) Annexe — Références rapides des méthodes

### Model — Players
- `list_players() -> List[Player]`
- `add_player(p: Player) -> bool`

### Model — Rounds & Matches
- `list_rounds() -> List[Round]`
- `create_round(name, number?, date?) -> Round`
- `add_match_to_round(round_id, white_id, black_id, board?) -> Optional[Match]`
- `set_match_result(round_id, match_id, result?) -> bool`
- `list_matches_for_round(round_id) -> List[Match]`

### View (extraits)
- `ask_yes_no(msg) -> bool`
- `prompt_player_fields() -> Dict[str, Any]`
- `prompt_round_fields() -> Dict[str, Any]`
- `prompt_match_fields() -> Dict[str, Any]`
- `select_round(rounds: List[Round]) -> Optional[str]`
- `show_players(...)`, `show_rounds(...)`, `show_player_added(...)`, `show_match_added(...)`, `show_set_result(...)`

### Controller
- `flow_players()`
- `flow_rounds()`
- `main_cli()`

---

## 15) FAQ technique

**Q : Pourquoi ne pas sérialiser directement des `dataclass` en JSON ?**  
R : Pour conserver la **maîtrise** du format (rétrocompatibilité, clés optionnelles, régénération d’UUID…).

**Q : L’écriture atomique suffit-elle ?**  
R : Oui contre les JSON corrompus, **non** contre les compétitions d’écriture multi-processus. Ajouter un verrou si nécessaire.

**Q : Comment importer ce document dans Google Docs ?**  
R : Dans Google Drive → *Nouveau* → *Importer un fichier* → sélectionner ce `.md`. Google Docs l’ouvrira et permettra d’éditer/mettre en forme.  
(Alternativement, je peux fournir une version `.docx` sur demande.)

