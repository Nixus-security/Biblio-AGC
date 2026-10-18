# ADR 0002 : SQLite plutôt qu'un serveur de base de données

- Statut : proposé
- Date : 2026-10-07
- Décideurs : Nixus-security

## Contexte
Biblio gère les prêts d'une petite bibliothèque associative : quelques centaines de livres, une poignée d'adhérents, un seul poste d'utilisation à la fois. L'application est une ligne de commande en Python, installée par des bénévoles qui ne sont pas administrateurs système. Il faut donc choisir où stocker livres, adhérents et prêts, avec le moins de contraintes d'installation et de maintenance possible.

## Options envisagées
1. **SQLite (fichier local, module `sqlite3` de la bibliothèque standard Python)**
   - Pour : aucune installation ni service à administrer, un seul fichier `biblio.db` facile à sauvegarder, SQL complet, transactions, zéro dépendance externe.
   - Contre : peu adapté à de nombreux accès concurrents en écriture, pas d'accès réseau natif, pas de gestion fine des droits utilisateurs.
2. **Serveur PostgreSQL ou MySQL**
   - Pour : accès simultané depuis plusieurs postes, gestion des droits, outils d'administration et de sauvegarde matures.
   - Contre : un serveur à installer, configurer, sécuriser et maintenir, disproportionné pour l'usage ; les tests et la CI deviennent plus lourds.
3. **Fichiers plats (CSV ou JSON)**
   - Pour : très simple, lisible à la main.
   - Contre : pas de requêtes ni de contraintes d'intégrité, risque de corruption à l'écriture, il faut réécrire soi-même la logique de recherche et de jointure.

## Décision
Nous stockons les données dans une base SQLite locale (`biblio.db`, chemin modifiable via la variable d'environnement `BIBLIO_DB`).

## Conséquences
- Plus facile : installation immédiate (Python suffit), tests isolés avec une base temporaire, sauvegarde par simple copie du fichier.
- Plus difficile : si l'association veut un jour utiliser Biblio depuis plusieurs postes en même temps, il faudra migrer vers un serveur et adapter le code d'accès aux données.
- Négatif : SQLite n'applique pas les clés étrangères par défaut (`PRAGMA foreign_keys`), donc l'intégrité des données (adhérent inexistant, par exemple) doit être vérifiée dans le code.
- Négatif : la base est un fichier non chiffré ; toute personne ayant accès au poste peut le lire ou le modifier.
