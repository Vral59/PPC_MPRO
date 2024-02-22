# PPC MPRO Projet
Réalisation d’un mini solveur de CSP binaires

## Structure du fichier CSP

Le fichier CSP suit la structure suivante :

- `n = [Entier]`: Définit le nombre de variables.
- `m = [Entier]`: Définit le nombre de contraintes.
- `[ligne vide]`
- `[nom de la variable] = {[Domaine des solutions valides]}`: Définit les variables du problème avec leurs domaines.
- `[ligne vide]`
- `C-[nom de la variable 1 concerné]-[nom de la variable 2 concerné] = {[tuple de valeurs possibles], [tuple de valeurs possibles],...}`: Spécifie les contraintes binaires entre les variables.
