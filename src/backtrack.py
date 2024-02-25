import arc_consistency
import random
from typing import Dict, Tuple, Union, List
import time

def backtrack(
    variables: Dict[str, List[int]],
    constraints: Dict[Tuple[str, str], List[Tuple[int, int]]],
    MAC3: bool = False,
    MAC4: bool = False,
    FW: bool = False,
    RMAC: bool = False,
    pick_var: str = "smallest_ind",
    pick_val: str = "smallest", 
    time_limit: int = 600
) -> Union[Tuple[Dict[str, int], int], Tuple[None, None]]:
    """
    Algorithme de retour en arrière pour résoudre un CSP.

    :param variables: Dictionnaire des variables et des domaines.
    :param constraints: Dictionnaire des contraintes binaires.
    :param MAC3: Activation ou désactivation de l'algorithme MAC avec AC3.
    :param MAC4: Activation ou désactivation de l'algorithme MAC avec AC4.
    :param FW: Activation ou désactivation du FordWard Checking.
    :param RMAC: Activation ou désactivation de l'algorithme MAC sur la racine uniquement.
    :param pick_var: Heuristique de choix sur les variables.
    :param pick_val: Heuristique de choix sur les valeurs.
    :return: Une solution valide ou None.
    """
    start_time = time.time()
    # Vérifier si pick_var est une valeur valide
    valid_pick_var_options = ["smallest_ind", "biggest_ind", "smallest_domain", "largest_domain", "random",
                              "most_constrained", "least_constrained"]
    if pick_var not in valid_pick_var_options:
        raise ValueError(f"Valeur invalide pour pick_var. Attendue parmi {valid_pick_var_options}, obtenue {pick_var}")

    # Vérifier si pick_val est une valeur valide
    valid_pick_val_options = ["smallest", "biggest", "smallest_domain", "biggest_domain", "odd_even", "random"]
    if pick_val not in valid_pick_val_options:
        raise ValueError(f"Valeur invalide pour pick_val. Attendue parmi {valid_pick_val_options}, obtenue {pick_val}")

    solution: Dict[str, int] = {}  # Dictionnaire pour stocker les valeurs attribuées aux variables
    node: int = 0

    def apply_FW(x: str, a: int) -> None:
        """
        Applique le FordWard Checking pour réduire les domaines après avoir fixé <x, a>.
        """
        nonlocal variables
        nonlocal constraints

        for y in [nom for nom in variables if nom not in solution]:
            variables[y] = [b for b in variables[y] if check_FW(a, b, x, y)]

    def check_FW(a: int, b: int, x: str, y: str) -> bool:
        nonlocal variables
        nonlocal constraints

        if (x, y) in constraints:
            if (a, b) not in constraints[(x, y)]:
                return False
        if (y, x) in constraints:
            if (b, a) not in constraints[(y, x)]:
                return False
        return True

    def choose_variable() -> str:
        """
        Choisir la prochaine variable à assigner.
        """
        nonlocal variables
        nonlocal solution

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
                len(constraints[(v, n)]) for n in variables_non_attribuee if (v, n) in constraints) + sum(
                len(constraints[(n, v)]) for n in variables_non_attribuee if (n, v) in constraints))
        elif pick_var == 'least_constrained':
            return max(variables_non_attribuee, key=lambda v: sum(
                len(constraints[(v, n)]) for n in variables_non_attribuee if (v, n) in constraints) + sum(
                len(constraints[(n, v)]) for n in variables_non_attribuee if (n, v) in constraints))

    def order_values(variable: str) -> List[int]:
        """
        Ordonner les valeurs d'une variable selon l'heuristique choisie.
        """
        nonlocal variables
        nonlocal constraints
        nonlocal solution

        if pick_val == "smallest":
            return sorted(variables[variable])
        elif pick_val == "biggest":
            return sorted(variables[variable], reverse=True)
        elif pick_val == "smallest_domain": # nombre de fois ou la valeur apparait dans les contraintes
            return sorted(variables[variable], key=lambda v: sum(
                sum(1 for z in constraints[(x, y)] if v in z) for (x, y) in constraints))
        elif pick_val == "biggest_domain":
            return sorted(variables[variable], key=lambda v: sum(
                sum(1 for z in constraints[(x, y)] if v in z) for (x, y) in constraints), reverse=True)
        elif pick_val == 'odd_even':
            if len(solution) % 2 == 0:
                return sorted(variables[variable], reverse=True)
            else:   
                return sorted(variables[variable], reverse=True)
        elif pick_val == 'random':
            random.shuffle(variables[variable])
            return (variables[variable])

    def backtrack_recursive() -> bool:
        """
        Fonction récursive pour le retour en arrière.
        """
        nonlocal solution
        nonlocal variables
        nonlocal node

        nonlocal start_time
        if time.time() - start_time > time_limit:
            print("Timeout")
            return False
        
        ordered_values = list[int]
        if len(solution) == len(variables):
            return True  # Solution trouvée

        unassigned_variable = choose_variable()

        if unassigned_variable is not None:
            ordered_values = order_values(unassigned_variable)

        for valeur in ordered_values:
            solution[unassigned_variable] = valeur
            node += 1

            saved_variables = variables.copy()
            if FW:
                apply_FW(unassigned_variable, valeur)
            elif MAC3:
                for el in solution:
                    variables[el] = [solution[el]]
                variables, _ = arc_consistency.ac3(variables, constraints)
            elif MAC4:
                for el in solution:
                    variables[el] = [solution[el]]
                _, variables = arc_consistency.ac4(variables, constraints)
                # variables, _ = arc_consistency.ac4_old(variables, constraints)

            elif RMAC and len(solution) == 1:
                el = next(iter(solution))  # Obtenez le seul élément du dictionnaire
                variables[el] = [solution[el]]
                variables, _ = arc_consistency.ac3(variables, constraints)

            if verifie_contraintes():
                if backtrack_recursive():
                    return True

            del solution[unassigned_variable]
            variables = saved_variables

        return False

    def verifie_contraintes() -> bool:
        """
        Vérifies si les contraintes sont respectées.
        """
        nonlocal solution
        nonlocal constraints

        for indices, valeurs in constraints.items():
            if indices[0] in solution and indices[1] in solution:
                val1, val2 = solution[indices[0]], solution[indices[1]]

                if (val1, val2) not in valeurs:
                    return False
        return True

    if backtrack_recursive():
        return solution, node
    else:
        return None, None
