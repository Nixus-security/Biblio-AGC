# ADR 0003 : requêtes SQL paramétrées

- Statut : proposé
- Date : 2026-10-07
- Décideurs : Nixus-security

## Contexte
Une bénévole a cherché « l'étranger » et le programme s'est fermé avec une erreur SQL. `search_books` construisait sa requête en concaténant le texte saisi (`"... LIKE '%" + text + "%'"`). Une apostrophe casse la requête, et le même défaut permet une injection SQL : un utilisateur peut faire exécuter du SQL de son choix. Il faut fixer une règle pour toutes les requêtes du projet, car plusieurs fonctions reçoivent des valeurs saisies par l'utilisateur.

## Options envisagées
1. **Concaténer le texte et l'échapper à la main** (doubler les apostrophes)
   - Pour : aucun changement de structure du code.
   - Contre : facile à oublier ou à mal faire, la protection dépend de chaque développeur, des cas limites subsistent.
2. **Requêtes paramétrées (`?` avec un tuple de valeurs, via `sqlite3`)**
   - Pour : le pilote sépare la requête et les données, donc plus d'injection ni d'erreur sur les apostrophes ; déjà utilisé dans `list_books`, `borrow_book` et `return_book` ; aucune dépendance en plus.
   - Contre : demande de la discipline à chaque nouvelle requête ; les noms de tables ou de colonnes ne peuvent pas être paramétrés.
3. **Utiliser un ORM (par exemple SQLAlchemy)**
   - Pour : l'accès aux données est abstrait et les requêtes sont paramétrées par défaut.
   - Contre : dépendance externe lourde pour un petit projet, courbe d'apprentissage, installation plus longue pour les bénévoles.

## Décision
Toute valeur qui vient de l'utilisateur est passée à SQLite par un paramètre `?`, jamais concaténée dans la chaîne SQL.

## Conséquences
- Plus facile : la recherche accepte les apostrophes et les accents, l'injection SQL est évitée, et la relecture est simple (une concaténation dans une requête est refusée).
- Plus difficile : chaque nouvelle requête doit respecter la règle, rien ne l'impose automatiquement.
- Négatif : les caractères `%` et `_` saisis par l'utilisateur restent interprétés comme des jokers par `LIKE`. La recherche peut renvoyer plus de résultats que prévu.
- Négatif : un test dédié à l'injection n'existe pas encore ; sans lui, une régression pourrait passer inaperçue.
