# Circulation de l'information : groupe AGC

À compléter par le groupe en séance 1. Chaque section est rédigée et poussée par un membre différent.

## 1. Rôles
Rédigé par : @Nixus-security

Qui produit les issues, qui relit les pull requests, qui décide du merge.

- **Issues** : chaque membre ouvre les issues des bugs ou évolutions qu'il identifie, avec le bon modèle (bug, évolution, question). Personne n'est assigné à l'ouverture.
- **Relecture** : chaque pull request est relue par au moins un autre membre du groupe, désigné en Reviewer par l'auteur de la PR.
- **Merge** : l'auteur de la PR merge, uniquement après l'approbation du relecteur et la résolution des conversations. Personne ne merge sa propre PR sans approbation.
- **Branches** : un membre ne pousse jamais directement sur `main`.

## 2. Où circule chaque information
Rédigé par : @Nixus-security

| Information | Qui la produit | Qui la valide | Où elle est stockée | Durée de vie |
|---|---|---|---|---|
| Code source | Le membre qui code, sur une branche | Un autre membre, par relecture de la pull request | Dépôt GitHub, branche `main` (historique Git) | Permanente |
| Bug signalé | Le membre qui l'a constaté | Le membre qui trie : il reproduit le bug et confirme le label | Issues GitHub (modèle « Signaler un bug ») | Jusqu'à la fermeture de l'issue par la PR qui le corrige (`Closes #n`) |
| Décision technique | Le membre qui propose le choix | Un autre membre, par relecture de la PR de l'ADR | Dossier `docs/adr/`, un fichier par décision (ADR) | Permanente : une décision remplacée reste, avec le statut « remplacé par ADR XXXX » |
| Documentation d'installation | Le membre qui a lancé les commandes | Un autre membre, qui suit le README à la lettre | `README.md` dans le dépôt | Mise à jour à chaque changement d'installation ou d'utilisation |
| Question rapide entre membres | Le membre qui est bloqué | Le membre qui répond | Messagerie du groupe ; si la réponse sert à d'autres, issue « Poser une question » | Éphémère sur la messagerie ; conservée dans l'issue si elle a une valeur durable |
| Compte rendu de réunion | Le membre qui prend les notes | Tous les membres présents | `docs/` dans le dépôt, un fichier daté par réunion | Permanente |

## 3. Règles de l'équipe
Rédigé par : anthony nagul 

Format des titres d'issue, labels utilisés, qui trie, qui assigne.

- **Titres d'issue** : ce qui se passe et où, par exemple `La recherche plante sur un titre avec apostrophe`. Pas de « ça marche pas ».
- **Contenu d'une issue** : commit, système, version de Python, étapes numérotées depuis `python biblio.py init`, résultat attendu et résultat observé.
- **Labels** : `bug`, `evolution` et `question`, posés selon le modèle utilisé à l'ouverture.
- **Tri** : un membre trie les nouvelles issues, reproduit le bug et confirme ou corrige le label. Un comportement normal devient une question : on y répond, puis on la ferme.
- **Assignation** : personne n'est assigné à l'ouverture ; le membre qui prend le sujet s'assigne lui-même en créant sa branche.
- **Branches** : `fix/<n>-mot-cle` pour un bug, `docs/<n>-sujet` pour la documentation, avec `<n>` le numéro de l'issue.
- **Commits** : préfixe `fix:`, `docs:` ou `feat:`, puis un message court (`fix: refuse un livre deja emprunte`).
- **Pull requests** : un seul sujet par PR, `Closes #n` dans le Contexte, modèle rempli, un relecteur désigné.
Règle à partir de la séance 2 : aucun push direct sur main, tout passe par une pull request relue.
