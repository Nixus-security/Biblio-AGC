# Biblio

Biblio est un petit logiciel en ligne de commande pour gérer les prêts de livres d'une bibliothèque associative : lister les livres, les rechercher, enregistrer un emprunt ou un retour, et repérer les retards. Les données sont stockées dans une base SQLite locale.

## Prérequis

- Python 3 (testé avec Python 3.12).
- Git, pour récupérer le projet.
- Aucune bibliothèque externe : tout vient de la bibliothèque standard de Python (`sqlite3`).

Vérifiez votre version de Python :

```bash
python3 --version
```

```text
Python 3.12.3
```

Selon le système, la commande s'appelle `python`, `python3` (macOS et Linux) ou `py` (Windows). Dans la suite, remplacez `python` par celle qui fonctionne chez vous.

## Installation

1. Récupérez le projet :

```bash
git clone <URL-du-depot>
cd <dossier-du-depot>
```

2. Créez la base de données avec quelques livres et adhérents d'exemple :

```bash
python biblio.py init
```

```text
Base initialisee : 6 livres, 3 membres.
```

Le fichier `biblio.db` est créé dans le dossier courant. Relancer `init` efface la base et la remet à son état de départ.

Pour utiliser un autre fichier, définissez la variable d'environnement `BIBLIO_DB` :

```bash
BIBLIO_DB=/chemin/vers/ma-base.db python biblio.py init
```

## Utilisation

Lancer `python biblio.py` sans argument affiche l'aide.

### Lister les livres

```bash
python biblio.py livres
```

```text
[1] L'Etranger (Albert Camus) : disponible
[2] Dune (Frank Herbert) : emprunte
[3] Le Petit Prince (Antoine de Saint-Exupery) : disponible
[4] Fondation (Isaac Asimov) : disponible
[5] Les Miserables (Victor Hugo) : disponible
[6] Neuromancien (William Gibson) : disponible
```

### Chercher un livre par son titre

```bash
python biblio.py chercher dune
```

```text
[2] Dune (Frank Herbert)
```

Les accents et les apostrophes sont acceptés dans la recherche. Si rien ne correspond, le programme affiche `Aucun livre trouve.`

### Emprunter un livre

La commande prend le numéro du livre, puis celui de l'adhérent :

```bash
python biblio.py emprunter 3 2
```

```text
Emprunt enregistre : livre 3, membre 2.
```

Un livre déjà emprunté est refusé :

```bash
python biblio.py emprunter 3 1
```

```text
Erreur : livre 3 deja emprunte.
```

### Rendre un livre

```bash
python biblio.py rendre 2
```

```text
Retour enregistre pour le livre 2.
```

### Voir les retards

Un prêt est en retard au bout de 14 jours. Seuls les livres non rendus sont listés :

```bash
python biblio.py retards
```

```text
Dune, emprunte par Alice Martin : 256 jours de retard
```

Le nombre de jours dépend de la date du jour. Après le retour de Dune :

```bash
python biblio.py rendre 2
python biblio.py retards
```

```text
Retour enregistre pour le livre 2.
Aucun retard.
```

## Tests

Depuis la racine du projet :

```bash
python -m unittest
```

```text
....
----------------------------------------------------------------------
Ran 4 tests in 0.208s

OK
```

Les tests utilisent une base temporaire : ils ne modifient pas votre `biblio.db`. Les mêmes tests sont lancés automatiquement sur GitHub à chaque pull request (`.github/workflows/tests.yml`).

## Structure du projet

```text
.
├── biblio.py                     # le programme : base de données et commandes
├── tests/
│   └── test_biblio.py            # tests unitaires
├── docs/
│   ├── circulation.md            # rôles et circulation de l'information dans l'équipe
│   └── adr/                      # décisions techniques (un fichier par décision)
│       └── 0000-modele.md        # modèle à copier pour une nouvelle décision
├── exercices/                    # énoncés des séances
└── .github/
    ├── ISSUE_TEMPLATE/           # modèles d'issues : bug, évolution, question
    ├── pull_request_template.md  # modèle de pull request
    └── workflows/tests.yml       # tests automatiques
```

## Contribuer

1. **Ouvrez une issue** avec le bon modèle (« Signaler un bug », « Proposer une évolution » ou « Poser une question »), avec les étapes pour reproduire depuis `python biblio.py init`. Notez son numéro `n`.
2. **Partez de `main` à jour**, puis créez une branche :

```bash
git checkout main && git pull
git checkout -b fix/<n>-mot-cle
```

   Utilisez `fix/<n>-...` pour un bug et `docs/<n>-...` pour la documentation.
3. **Testez** avec `python -m unittest`, puis faites un commit avec un préfixe (`fix:`, `docs:`, `feat:`) :

```bash
git commit -m "fix: refuse un livre deja emprunte"
git push -u origin fix/<n>-mot-cle
```

4. **Ouvrez une pull request** vers `main` de votre dépôt, avec `Closes #n` dans le Contexte, le modèle rempli et un relecteur.
5. **Après l'approbation**, résolvez les conversations, mergez, puis supprimez la branche.

On ne pousse jamais directement sur `main`, et une pull request ne traite qu'un seul sujet. Les décisions techniques importantes sont notées dans `docs/adr/`. Les règles de l'équipe sont décrites dans [docs/circulation.md](docs/circulation.md).

## Auteurs

- [@Nixus-security](https://github.com/Nixus-security)
