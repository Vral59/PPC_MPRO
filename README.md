# PPC MPRO Projet
Ce projet vise à réaliser un mini solveur de CSP binaires.

## Structure du fichier CSP

Le fichier CSP suit la structure suivante :

- `n = [Entier]`: Définit le nombre de variables.
- `m = [Entier]`: Définit le nombre de contraintes.
- `[ligne vide]`
- `[nom de la variable] = {[Domaine des solutions valides]}`: Définit les variables du problème avec leurs domaines.
- `[ligne vide]`
- `C-[nom de la variable 1 concerné]-[nom de la variable 2 concerné] = {[tuple de valeurs possibles], [tuple de valeurs possibles],...}`: Spécifie les contraintes binaires entre les variables.

## Utilisations
Pour ce projet, aucun requirement externe n'est requis pour l'exécution, à part les modules déjà présents dans Python 3.10.

Vous pouvez ajuster les paramètres dans la fonction main() du fichier main.py pour résoudre différents problèmes disponibles.

## Structure du projet 
Structure du Projet

- `docs/` : Contient la documentation du projet générée avec Sphinx. Par exemple, dans `docs/build/html`, le fichier `index.html` récapitule la documentation.

- `instance/` : Contient des graphes et des exemples de CSP.

- `src/` : Contient le code source du projet, avec différents fichiers .py.

- `result/` : Contient les fichiers CSV récapitulant les résultats du projet.
## Exécution 
Pour exécuter le projet, utilisez la commande suivante dans votre terminal :
```bash
python main.py
```