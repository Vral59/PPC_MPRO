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

## Utilisation du fichier readcsp.py

Le fichier `readcsp.py` contient le code permettant de lire un fichier CSP au format décrit ci-dessus et de le convertir en une représentation utilisable en Python. L'exemple du cours 1 slide 12 est dans `instance\exemple_csp.txt`.

## Utilisation du fichier geninstance.py

Le fichier `geninstance.py` contient le code permettant de générer des instances. Pour l'instant uniquement celles du problème du placement de n reines.
