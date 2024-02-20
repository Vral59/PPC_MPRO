import random

def backtrack(variables, contraintes, FW=False):
    """
    Algorithme de backtrack pour résoudre un CSP

    :param variables: Dictionnaire des variables et des domaines.
    :param contraintes: Dictionnaire des variables et des contraintes binaires.
    :param FW: forward recursive.
    :return: Une solution valide ou None.
    """
    solution = {}  # Dictionnaire pour stocker les valeurs attribuées aux variables

    def check_FW(a, b, x, y):
        nonlocal variables
        nonlocal contraintes
        if (x, y) in contraintes :
            if (a, b) not in contraintes[(x, y)]:
                #print("y = ", y, "b = ", b)
                return False
        if (y, x) in contraintes :
            if (b, a) not in contraintes[(y, x)]:
                #print("y = ", y, "b = ", b)
                return False
        return True

    def apply_FW(solution, x, a):
        nonlocal variables
        nonlocal contraintes
        for y in [nom for nom in variables if nom not in solution] :
            variables[y] = [b for b in variables[y] if check_FW(a, b, x, y)]  
            
    def backtrack_recursive():
        #print("variables = ", variables)
        nonlocal solution
        nonlocal variables

        # Vérifier si toutes les variables ont une valeur attribuée
        if len(solution) == len(variables):
            return True  # Solution trouvée

        # Choisir une variable non attribuée
        variable_non_attribuee = [nom for nom in variables if nom not in solution][0]

        # Essayer chaque valeur du domaine de la variable
        for valeur in variables[variable_non_attribuee]:
            solution[variable_non_attribuee] = valeur

            saved_variables = variables.copy()
            if  FW:
                #print(" variables = ", variable_non_attribuee, " valeur = ", valeur)
                apply_FW(solution, variable_non_attribuee, valeur)

            # Vérifier si la solution partielle satisfait toutes les contraintes
            if verifie_contraintes():
                # Récursivement continuer avec la solution partielle
                if backtrack_recursive():
                    return True

            # Retirer la valeur si elle ne mène pas à une solution
            del solution[variable_non_attribuee]
            variables = saved_variables
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