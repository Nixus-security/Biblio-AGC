# ADR 0004 : convention de branches

- Statut : proposé
- Date : 2026-10-07
- Décideurs : Nixus-security

## Contexte
Trois personnes travaillent en même temps sur le même dépôt. À partir de la séance 2, aucun push direct sur `main` n'est autorisé : tout passe par une pull request relue. Il faut une convention de nommage et d'organisation des branches pour savoir qui travaille sur quoi, relier chaque branche à une issue, et garder `main` toujours utilisable.

## Options envisagées
1. **Travailler directement sur `main`**
   - Pour : aucune friction, pas de branche à gérer.
   - Contre : pas de relecture, un travail cassé arrive tout de suite chez les autres, historique difficile à lire.
2. **Une branche courte par sujet, nommée `type/<n>-mot-cle`, fusionnée par pull request** (`fix/<n>-...` pour un bug, `docs/<n>-...` pour la documentation)
   - Pour : le nom indique le type de travail et l'issue concernée ; relecture avant fusion ; `main` reste stable ; simple à expliquer.
   - Contre : demande de créer une branche et une PR même pour un petit changement ; des branches qui durent trop longtemps créent des conflits.
3. **Modèle Gitflow (`develop`, `release`, `hotfix`, `feature`)**
   - Pour : cadre précis pour des versions publiées régulièrement.
   - Contre : trop lourd pour une petite équipe et un projet sans cycle de versions.

## Décision
Une branche courte par sujet partant de `main`, nommée `fix/<n>-mot-cle` ou `docs/<n>-mot-cle` (avec `<n>` le numéro de l'issue), fusionnée dans `main` uniquement par pull request relue, puis supprimée.

## Conséquences
- Plus facile : chaque changement est relu et relié à une issue (`Closes #n`), `main` reste stable, et l'historique raconte qui a fait quoi.
- Plus difficile : même un petit changement demande une branche, une PR et un relecteur disponible.
- Négatif : une PR en attente de relecture bloque le sujet, et les branches qui restent ouvertes longtemps entraînent des conflits de fusion.
- Négatif : la règle repose sur la discipline de l'équipe tant que la protection de `main` n'est pas activée dans les réglages GitHub.
