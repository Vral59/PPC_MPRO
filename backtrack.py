import random


def backtrack(variables, contraintes, MAC=False, FW=False, RMAC=False, pick_var="smallest_ind", pick_val="smallest"):
    """
    Algorithme de backtrack pour résoudre un CSP

    :param variables: Dictionnaire des variables et des domaines.
    :param contraintes: Dictionnaire des variables et des contraintes binaires.
    :param MAC: Activation ou désactivation de l'algorithme MAC.
    :param FW: Activation ou désactivation du FordWard Checking.
    :param RMAC: Activation ou désactivation de l'algorithme MAC sur la racine uniquement.
    :param pick_var: Heuristique de choix sur les variables.
    :param pick_val: Heuristique de choix sur les Valeurs.
    :return: Une solution valide ou None.
    """
    solution = {}  # Dictionnaire pour stocker les valeurs attribuées aux variables
    # Fixation d'un seed pour l'aléatoire
    #seed_value = 42
    #random.seed(seed_value)

    if sum([MAC, RMAC, FW]) > 1:
        print("Ne fonctionne pas avec plusieurs en True")
        return None

    def apply_FW(solution, x, a):
        """
        Applique le FordWard Checking pour réduire les domaines après avoir fixé <x, a>.
        """
        nonlocal variables
        nonlocal contraintes
        for y in [nom for nom in variables if nom not in solution]:
            variables[y] = {b for b in variables[y] if check_FW(a, b, x, y)}

    def maintain_ac4_consistency(x, a):
        """
        Application de l'algorithme MAC avec un AC4
        """
        nonlocal variables
        nonlocal contraintes
        Q = set()  # Ensemble Q pour stocker les paires (y, b) à traiter
        S = {}  # Dictionnaire S pour stocker les paires (y, b) liées à d'autres variables

        # Identification des arcs impactés
        # Parcourir toutes les contraintes binaires
        for c, valeurs in contraintes.items():
            y1, y2 = c
            # Si x est impliqué dans la contrainte
            if y1 == x or y2 == x:
                # Ajouter les valeurs de la variable y1 qui ne satisfont pas la contrainte
                for b1 in variables[y1]:
                    if (a, b1) not in valeurs:
                        Q.add((y1, b1))
                # Ajouter les valeurs de la variable y2 qui ne satisfont pas la contrainte
                for b2 in variables[y2]:
                    if (a, b2) not in valeurs:
                        Q.add((y2, b2))

        # Propagation de l'arc-consistance
        while Q:
            y, b = Q.pop()
            # Pour chaque autre variable non attribuée
            for other_y in [nom for nom in variables if nom != y and nom not in solution]:
                # Pour chaque valeur de l'autre variable
                for other_b in variables[other_y]:
                    # Si la contrainte entre (y, b) et (other_y, other_b) existe
                    if (y, b) in contraintes.get((other_y, other_b), set()):
                        # Ajouter (y, b) à S et (other_y, other_b) à Q
                        if (other_y, other_b) not in S:
                            S[(other_y, other_b)] = set()
                        S[(other_y, other_b)].add((y, b))
                        Q.add((other_y, other_b))

        # Réduction des domaines
        for y, b in S.keys():
            # Si la valeur b dans le domaine de la variable y n'est liée à aucune autre variable
            if len(S[(y, b)]) == 0 and b in variables[y]:
                # Supprimer b du domaine de la variable y
                variables[y].remove(b)

    def check_FW(a, b, x, y):
        nonlocal variables
        nonlocal contraintes
        if (x, y) in contraintes:
            if (a, b) not in contraintes[(x, y)]:
                return False
        if (y, x) in contraintes:
            if (b, a) not in contraintes[(y, x)]:
                return False
        return True

    def choose_variable():
        """
        Vérifie si le FordWard Checking est satisfait pour les valeurs a et b et les variables x et y.
        """
        variables_non_attribuee = {nom for nom in variables if nom not in solution}
        if pick_var == "smallest_ind":
            return min(variables_non_attribuee)
        elif pick_var == "biggest_ind":
            return max(variables_non_attribuee)
        elif pick_var == "smallest_domain":
            return min(variables_non_attribuee, key=lambda v: len(variables[v]))
        elif pick_var == "largest_domain":
            return max(variables_non_attribuee, key=lambda v: len(variables[v]))
        elif pick_var == "random":
            return random.choice(list(variables_non_attribuee))
        elif pick_var == 'most_constrained':
            return min(variables_non_attribuee, key=lambda v: sum(
                len(contraintes[(v, nom)]) for nom in variables_non_attribuee if (v, nom) in contraintes) + sum(
                len(contraintes[(nom, v)]) for nom in variables_non_attribuee if (nom, v) in contraintes))
        elif pick_var == 'least_constrained':
            return max(variables_non_attribuee, key=lambda v: sum(
                len(contraintes[(v, nom)]) for nom in variables_non_attribuee if (v, nom) in contraintes) + sum(
                len(contraintes[(nom, v)]) for nom in variables_non_attribuee if (nom, v) in contraintes))

    def order_values(variable):
        """
        Permet d'indiquer comment choisir les variables
        """
        if pick_val == "smallest":
            return sorted(variables[variable])
        elif pick_val == "biggest":
            return sorted(variables[variable], reverse=True)
        elif pick_val == "smallest_domain":
            return sorted(variables[variable], key=lambda v: sum(
                sum(1 for z in contraintes[(x, y)] if v in z) for (x, y) in contraintes))
        elif pick_val == "biggest_domain":
            return sorted(variables[variable], key=lambda v: sum(
                sum(1 for z in contraintes[(x, y)] if v in z) for (x, y) in contraintes), reverse=True)

    def backtrack_recursive():
        global valeurs_ordonees
        nonlocal solution
        nonlocal variables

        if len(solution) == len(variables):
            return True  # Solution trouvée

        variable_non_attribuee = choose_variable()

        if variable_non_attribuee is not None:
            valeurs_ordonees = order_values(variable_non_attribuee)

        for valeur in valeurs_ordonees:
            solution[variable_non_attribuee] = valeur

            saved_variables = variables.copy()
            if FW:
                apply_FW(solution, variable_non_attribuee, valeur)
            elif MAC:
                maintain_ac4_consistency(variable_non_attribuee, valeur)
            elif RMAC and len(solution) == 1:
                maintain_ac4_consistency(variable_non_attribuee, valeur)

            if verifie_contraintes():
                if backtrack_recursive():
                    return True

            del solution[variable_non_attribuee]
            variables = saved_variables

        return False

    def verifie_contraintes():
        """
        Vérifies si les contraintes sont respectées
        """
        for indices, valeurs in contraintes.items():
            if indices[0] in solution and indices[1] in solution:
                val1, val2 = solution[indices[0]], solution[indices[1]]

                # Vérifier que les valeurs sont dans les contraintes réduites par AC4
                if (val1, val2) not in valeurs:
                    return False
        return True

    if backtrack_recursive():
        return solution
    else:
        return None
