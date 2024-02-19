import random

def backtrack(variables, contraintes):
    """
    Algorithme de backtrack pour résoudre un CSP

    :param variables: Dictionnaire des variables et des domaines.
    :param contraintes: Dictionnaire des variables et des contraintes binaires.
    :return: Une solution valide ou None.
    """
    solution = {}  # Dictionnaire pour stocker les valeurs attribuées aux variables

    def backtrack_recursive():
        nonlocal solution

        # Vérifier si toutes les variables ont une valeur attribuée
        if len(solution) == len(variables):
            return True  # Solution trouvée

        # Choisir une variable non attribuée
        variable_non_attribuee = [nom for nom in variables if nom not in solution][0]

        # Essayer chaque valeur du domaine de la variable
        for valeur in variables[variable_non_attribuee]:
            solution[variable_non_attribuee] = valeur

            # Vérifier si la solution partielle satisfait toutes les contraintes
            if verifie_contraintes():
                # Récursivement continuer avec la solution partielle
                if backtrack_recursive():
                    return True

            # Retirer la valeur si elle ne mène pas à une solution
            del solution[variable_non_attribuee]

        return False

    def verifie_contraintes():
        # Vérifier chaque contrainte
        for indices, valeurs in contraintes.items():
            if indices[0] in solution and indices[1] in solution:
                if (solution[indices[0]], solution[indices[1]]) not in valeurs:
                    return False
        return True

    keys = list(variables.keys())
    random.shuffle(keys)
    # Appel de la fonction de backtrack récursive
    if backtrack_recursive():
        return solution
    else:
        return None  # Aucune solution trouvée