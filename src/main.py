from src import backtrack, arc_consistency, generate_instance, read_csp
import time


def solve_nqueens(n: int, save_file: bool = False, file_name: str = "instance/queens_csp.txt",
                  use_MAC: bool = False, use_FW: bool = False, use_RMAC: bool = False,
                  pick_var: str = "smallest_domain", pick_val: str = "smallest") -> None:
    """
    Résout le problème des n reines en utilisant l'approche CSP.

    :param n : Taille du plateau en n*n.
    :param save_file: True s'il faut sauvegarder le CSP dans un txt.
    :param file_name: Chemin où enregistrer le CSP.
    :param use_MAC: Activation ou désactivation de l'algorithme MAC.
    :param use_FW: Activation ou désactivation du FordWard Checking.
    :param use_RMAC: Activation ou désactivation de l'algorithme MAC sur la racine uniquement.
    :param pick_var: Heuristique de choix sur les variables.
    :param pick_val: Heuristique de choix sur les valeurs.
    """
    # Vérifier que seulement un des trois algorithmes est activé
    if sum([use_MAC, use_FW, use_RMAC]) > 1:
        raise ValueError("Au maximum, un seul des use_MAC, use_FW, ou use_RMAC peut être à True.")

    # Générer le CSP pour le problème des n queens
    if save_file:
        # Création d'un CSP
        print("Création du CSP")
        generate_instance.generate_queens_csp(n, file_name)
        # Lecture du CSP
        print("Lecture du CSP")
        n, m, variables, constraints = read_csp.read_csp_file(file_name)
    else:
        n, m, variables, constraints = generate_instance.generate_queens_dict(n)

    # Résoudre le problème en utilisant l'algorithme de backtrack selon les paramètres
    start_time = time.time()
    result, nodes = backtrack.backtrack(variables, constraints,
                                        MAC=use_MAC, FW=use_FW, RMAC=use_RMAC,
                                        pick_var=pick_var, pick_val=pick_val)
    end_time = time.time()

    # Afficher les résultats
    if result is None:
        print(f"Aucune solution trouvée pour le problème des n-queens avec n={n}.")
    else:
        print(f"Solution pour le problème des n-queens avec n={n} : {result}")
        print(f"Temps d'exécution : {end_time - start_time} secondes")
        print(f"Nombre de nœuds explorés : {nodes}")
        print(f"Paramètres utilisés : use_MAC={use_MAC}, use_FW={use_FW}, use_RMAC={use_RMAC}, pick_var={pick_var}, "
              f"pick_val={pick_val}")


def solve_carrosserie() -> None:
    """
    Démonstration de l'utilisation de l'AC3 et l'AC4 sur le problème de carrosserie.
    """
    # Lecture du CSP du problème de carrosserie
    file_path = "../instance/carrosserie.txt"
    n, m, variables, constraints = read_csp.read_csp_file(file_path)

    start_time_ac3 = time.time()
    variables_ac3, constraints_ac3 = arc_consistency.ac3(variables, constraints)
    end_time_ac3 = time.time()
    start_time_ac4 = time.time()
    variables_ac4, constraints_ac4 = arc_consistency.ac4(variables, constraints)
    end_time_ac4 = time.time()

    print(f"Variables et domaines de base : {variables}")
    print(f"Variables et domaines avec l'AC3 : {variables_ac3}")
    print(f"Temps d'exécution de l'AC3 : {end_time_ac3 - start_time_ac3} secondes")
    print(f"Variables et domaines avec l'AC4 : {variables_ac4}")
    print(f"Temps d'exécution de l'AC4 : {end_time_ac4 - start_time_ac4} secondes")


def solve_coloration(k: int, graph_path: str, save_file: bool = False,
                     output_file_path: str = "../instance/graph_csp.txt",
                     use_MAC: bool = False, use_FW: bool = False, use_RMAC: bool = False,
                     pick_var: str = "random", pick_val: str = "smallest") -> None:
    """
    Résolution d'un problème de k coloration d'un graphe.

    :param k: Nombre de couleurs utilisable.
    :param graph_path: Chemin vers le graphe en format DIMACS.
    :param save_file: True s'il faut sauvegarder le CSP dans un txt.
    :param output_file_path: Chemin vers le fichier DIMACS du graphe.
    :param use_MAC: Activation ou désactivation de l'algorithme MAC.
    :param use_FW: Activation ou désactivation du FordWard Checking.
    :param use_RMAC: Activation ou désactivation de l'algorithme MAC sur la racine uniquement.
    :param pick_var: Heuristique de choix sur les variables.
    :param pick_val: Heuristique de choix sur les valeurs.
    """

    # Lire le graphe depuis un fichier au format DIMACS
    num_vertices, num_edges, graph = generate_instance.read_graph_dimacs(graph_path)

    # Vérifier que seulement un des trois algorithmes est activé
    if sum([use_MAC, use_FW, use_RMAC]) > 1:
        raise ValueError("Exactly one of use_MAC, use_FW, or use_RMAC should be True.")

    if save_file:
        # Générer le CSP pour le problème de coloration de graphe
        generate_instance.generate_graph_csp(graph, num_vertices, num_edges, k, output_file_path)

        # Lire le CSP généré
        n, m, variables, constraints = read_csp.read_csp_file(output_file_path)

    else:
        n, m, variables, constraints = generate_instance.generate_graph_dict(graph, k)

    # Résolution du problème avec l'algorithme de backtrack selon les paramètres
    start_time = time.time()
    result, nodes = backtrack.backtrack(variables, constraints,
                                        MAC=use_MAC, FW=use_FW, RMAC=use_RMAC,
                                        pick_var=pick_var, pick_val=pick_val)
    end_time = time.time()

    # Afficher les résultats
    if result is None:
        print(f"Aucune solution trouvée pour le problème de coloration de graphe avec {k} couleurs.")
    else:
        print(f"Solution pour le problème de coloration du graphe {graph_path} : ", result)
        print(f"Temps d'exécution : {end_time - start_time} secondes")
        print(f"Nombre de nœuds explorés : {nodes}")

    # Afficher les paramètres utilisés
    print(f"Paramètres utilisés : use_MAC={use_MAC}, use_FW={use_FW}, use_RMAC={use_RMAC}, pick_var={pick_var}, "
          f"pick_val={pick_val}")


def main():
    # Test des n reines avec différentes valeurs de taille de plateau.
    for n_value in [10, 20]:
        print(f"\nTest des n reines avec n={n_value}")
        solve_nqueens(n_value, use_FW=True, pick_var="smallest_domain", pick_val="smallest")

    print("\nTest carrosserie problème:")
    solve_carrosserie()

    print("\nTesting graph coloring problem:")
    graph_path = "../instance/DIMACS Graphs/huck.col"
    k_value = 11
    solve_coloration(k_value, graph_path, use_RMAC=True, pick_var="random", pick_val="smallest")


if __name__ == "__main__":
    main()
