from typing import Dict, List, Set, Tuple


def generate_queens_csp(n: int, file_path: str) -> None:
    """
    Crée un CSP binaire au format .txt pour le problème des n reines.

    :param n: Taille du plateau n*n.
    :param file_path: Chemin pour stocker le futur fichier .txt.
    """
    try:
        with open(file_path, "w") as output_file:
            output_file.write(f"n = {n}\n")
            output_file.write(f"m = {int(n * (n - 1) / 2)}\n\n")

            for i in range(1, n + 1):
                output_file.write(f"{i} = {{{','.join(map(str, range(1, n + 1)))}}}\n")

            output_file.write("\n")

            for i in range(1, n + 1):
                for j in range(i + 1, n + 1):
                    constraint_name = f"C-{i}-{j}"
                    constraint_values = [(c_i, c_j) for c_i in range(1, n + 1) for c_j in range(1, n + 1) if
                                         c_j - c_i != j - i and c_i - c_j != j - i and c_i != c_j]
                    output_file.write(f"{constraint_name} = {{{','.join(map(str, constraint_values))}}}\n")
    except Exception as e:
        print(f"Error: {e}")


def read_graph_dimacs(file_path: str) -> Tuple[int, int, Dict[int, List[int]]]:
    """
    Ouvre un fichier au format DIMACS représentant un graphe et crée un dictionnaire du graphe.

    :param file_path: Chemin vers le fichier DIMACS.
    :return: Un tuple contenant le nombre de sommets, le nombre d'arêtes et le dictionnaire représentant le graphe.
    """
    try:
        graph = {}

        with open(file_path, 'r') as file:
            lines = file.readlines()

            for line in lines:
                if line.startswith('c'):
                    continue

                if line.startswith('p'):
                    _, _, nb_vertices, nb_edges = line.split()
                    nb_vertices, nb_edges = int(nb_vertices), int(nb_edges)
                    break

            for i in range(1, nb_vertices + 1):
                graph[i] = []

            for line in lines:
                if line.startswith('e'):
                    _, vertex1, vertex2 = line.split()
                    vertex1, vertex2 = int(vertex1), int(vertex2)
                    graph[vertex1].append(vertex2)
                    graph[vertex2].append(vertex1)

        return nb_vertices, nb_edges, graph
    except Exception as e:
        print(f"Error: {e}")
        return 0, 0, {}


def generate_graph_csp(graph: Dict[int, List[int]], n: int, m: int, k: int, output_file: str) -> None:
    """
    Génère un CSP au format .txt pour le problème de coloration d'un graphe.

    :param graph: Dictionnaire représentant le graphe.
    :param n: Nombre de sommets dans le graphe.
    :param m: Nombre d'arêtes dans le graphe.
    :param k: Nombre de couleurs disponibles.
    :param output_file: Chemin vers le fichier de sortie du CSP.
    """
    try:
        with open(output_file, 'w') as file:
            file.write(f'n = {n}\n')
            file.write(f'm = {2 * m}\n\n')

            for node in range(1, n + 1):
                file.write(f"{node} = {{{','.join(map(str, range(1, k + 1)))}}}\n")

            file.write('\n')

            for node, neighbors in graph.items():
                for neighbor in neighbors:
                    file.write(f'C-{node}-{neighbor} = {{')
                    for i in range(1, k + 1):
                        for j in range(1, k + 1):
                            if i != j:
                                file.write(f'({i}, {j}), ')
                    file.seek(file.tell() - 2)
                    file.write('}\n')
    except Exception as e:
        print(f"Error: {e}")


def generate_queens_dict(n: int) -> Tuple[int, int, Dict[str, List[int]], Dict[Tuple[str, str], List[Tuple[int, int]]]]:
    """
    Génère les structures nécessaires pour le problème des n reines sans créer de fichier.

    :param n: Taille du plateau n*n.
    :return: Le nombre de variables, le nombre de contraintes, un dictionnaire de domaines de variables et un dictionnaire de tuples variables-valeurs.
    """
    variables = {}
    constraints = {}

    n_variables = n
    m_constraints = int(n * (n - 1) / 2)

    for i in range(1, n + 1):
        variable_name = str(i)
        variable_domain = list(range(1, n + 1))
        variables[variable_name] = variable_domain

    constraint_id = 1
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            concerned_variables = (str(i), str(j))
            valid_tuples = [(c_i, c_j) for c_i in range(1, n + 1) for c_j in range(1, n + 1) if
                            c_j - c_i != j - i and c_i - c_j != j - i and c_i != c_j]
            constraints[concerned_variables] = valid_tuples
            constraint_id += 1

    return n_variables, m_constraints, variables, constraints


def generate_graph_dict(graph: Dict[int, List[int]], k: int) -> \
        Tuple[int, int, Dict[str, List[int]], Dict[Tuple[str, str], List[Tuple[int, int]]]]:
    """
    Génère les structures nécessaires pour le problème de coloration de graphe sans créer de fichier.

    :param graph: Dictionnaire représentant le graphe.
    :param k: Nombre de couleurs disponibles.
    :return: Le nombre de variables, le nombre de contraintes, un dictionnaire de domaines de variables et un dictionnaire de tuples variables-valeurs.
    """
    variables = {}
    constraints = {}

    n_variables = len(graph)
    m_constraints = sum(len(neighbors) for neighbors in graph.values())

    for node in graph:
        variable_name = str(node)
        variable_domain = list(range(1, k + 1))
        variables[variable_name] = variable_domain

    constraint_id = 1
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            concerned_variables = (str(node), str(neighbor))
            valid_tuples = [(i, j) for i in range(1, k + 1) for j in range(1, k + 1) if i != j]
            constraints[concerned_variables] = valid_tuples
            constraint_id += 1

    return n_variables, m_constraints, variables, constraints


def add_all_diff(variables: Dict[str, Set[int]], constraints: Dict[Tuple[str, str], Set[Tuple[int, int]]], x1: str,
                 x2: str) -> None:
    """
    Ajoute une contrainte 'toutes différentes' entre deux variables.

    :param variables: Dictionnaire de domaines de variables.
    :param constraints: Dictionnaire de contraintes.
    :param x1: Première variable.
    :param x2: Deuxième variable.
    """
    l1 = {(a, b) for a in variables[x1] for b in variables[x2] if a != b}
    if (x1, x2) in constraints:
        constraints[(x1, x2)] = l1.intersection(constraints[(x1, x2)])
    elif (x2, x1) in constraints:
        constraints[(x2, x1)] = l1.intersection(constraints[(x2, x1)])
    else:
        constraints[(x1, x2)] = l1


def add_c1_smaller_c2(variables: Dict[str, Set[int]], constraints: Dict[Tuple[str, str], Set[Tuple[int, int]]], x1: str,
                      x2: str) -> None:
    """
    Ajoute une contrainte indiquant que x1 est inférieur à x2.

    :param variables: Dictionnaire de domaines de variables.
    :param constraints: Dictionnaire de contraintes.
    :param x1: Première variable.
    :param x2: Deuxième variable.
    """
    l1 = {(a, b) for a in variables[x1] for b in variables[x2] if a < b}
    if (x1, x2) in constraints:
        constraints[(x1, x2)] = l1.intersection(constraints[(x1, x2)])
    elif (x2, x1) in constraints:
        constraints[(x2, x1)] = l1.intersection(constraints[(x2, x1)])
    else:
        constraints[(x1, x2)] = l1
