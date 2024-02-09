
def lire_fichier_csp(chemin_fichier):
    """
    Permet de lire un csp dans un format particulier et de le stocker
    :param chemin_fichier: Chemin vers le fichier .txt
    :return: Le nombre de variables, le nombre de contraintes, un dictionnaire variables domaine et un dictionnaire
    tuples variables et valeurs
    """
    variables = {}
    contraintes = {}

    try:
        with open(chemin_fichier, 'r') as fichier:
            lignes = fichier.readlines()

            if len(lignes) < 4:
                raise ValueError("Le fichier ne contient pas suffisamment de lignes.")

            n = int(lignes[0].strip().split('=')[1])
            m = int(lignes[1].strip().split('=')[1])

            ligne_actuelle = 3  # On saute les deux premières lignes et la ligne vide
            for i in range(n):
                if ligne_actuelle >= len(lignes):
                    raise ValueError("Nombre insuffisant de lignes pour les variables.")

                ligne = lignes[ligne_actuelle].strip().split('=')
                if len(ligne) == 2:
                    nom_variable = ligne[0].strip()
                    domaine = eval(ligne[1].strip())  # Utilisation de eval pour traiter les ensembles
                    variables[nom_variable] = domaine
                    ligne_actuelle += 1
                else:
                    raise ValueError("Format invalide pour la définition d'une variable.")

            ligne_actuelle += 1  # On saute la ligne vide après les variables

            for j in range(m):
                if ligne_actuelle >= len(lignes):
                    raise ValueError("Nombre insuffisant de lignes pour les contraintes.")

                ligne = lignes[ligne_actuelle].strip().split('=')
                if len(ligne) == 2:
                    variables_concernees = tuple(map(str, ligne[0].strip().split('-')[1:]))
                    tuples_valides = eval(ligne[1].strip())  # Utilisation de eval pour traiter les ensembles
                    contraintes[variables_concernees] = tuples_valides
                    ligne_actuelle += 1
                else:
                    raise ValueError("Format invalide pour la définition d'une contrainte.")

    except (IOError, ValueError, SyntaxError) as e:
        print(f"Erreur lors de la lecture du fichier : {str(e)}")
        return None, None, None, None

    return n, m, variables, contraintes
