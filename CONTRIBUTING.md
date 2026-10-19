# Contribuer à Biblio-AGC

Merci de prendre le temps de contribuer. Ce guide explique comment signaler un problème, proposer une évolution et soumettre une pull request.

## Avant de commencer

- Vérifiez que votre version de Python est 3.10 ou supérieure : `python3 --version`
- Clonez le dépôt et créez la base d'exemple : `python biblio.py init`
- Lancez les tests pour vous assurer que tout passe : `python -m unittest`

## Signaler un bug ou proposer une évolution

Ouvrez une issue avec le bon modèle (disponibles dans l'onglet Issues → New issue) :

- **Signaler un bug** — décrivez les étapes pour reproduire depuis `python biblio.py init`
- **Proposer une évolution** — décrivez le besoin, pas la solution
- **Poser une question** — si vous n'êtes pas sûr de la bonne catégorie
- **Signaler un blocage** — si vous êtes bloqué et avez besoin d'aide d'un camarade

Notez le numéro `#n` de votre issue : vous en aurez besoin pour nommer la branche.

## Créer une branche

Partez toujours de `main` à jour :

```bash
git checkout main
git pull
git checkout -b fix/<n>-mot-cle    # pour un bug
git checkout -b feat/<n>-mot-cle   # pour une nouvelle fonctionnalité
git checkout -b docs/<n>-mot-cle   # pour la documentation
```

## Conventions de commit

Préfixez chaque message avec le type de changement :

| Préfixe | Usage |
|---------|-------|
| `fix:`  | correction d'un bug |
| `feat:` | nouvelle fonctionnalité |
| `docs:` | documentation uniquement |
| `test:` | ajout ou correction de tests |
| `chore:` | maintenance (dépendances, CI…) |

Exemple : `git commit -m "fix: refuse un livre déjà emprunté"`

## Soumettre une pull request

1. Poussez votre branche : `git push -u origin <votre-branche>`
2. Ouvrez une PR vers `main` depuis l'interface GitHub
3. Remplissez le modèle de PR (contexte, changements, impact, comment tester, checklist)
4. Ajoutez `Closes #n` dans le champ Contexte
5. Désignez au moins un relecteur

## Definition of Done

Une PR est prête à merger quand :

- [ ] Les tests passent (`python -m unittest`)
- [ ] La PR traite un seul sujet
- [ ] La documentation concernée est à jour
- [ ] Au moins une approbation de review a été obtenue
- [ ] Toutes les conversations de review sont résolues

## Après le merge

Supprimez votre branche locale et distante :

```bash
git checkout main
git pull
git branch -d <votre-branche>
git push origin --delete <votre-branche>
```

On ne pousse **jamais** directement sur `main`.
