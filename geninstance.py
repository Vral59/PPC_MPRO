def generate_queens_csp(n, chemin_fichier):
    """
    Création d'un csp binaire en .txt pour le problème des n reines
    :param n: taille du plateau n*n
    :param chemin_fichier: Chemin vers le stockage du futur .txt
    """
    # Création du fichier de sortie
    output_file = open(chemin_fichier, "w")

    # Écriture des dimensions des variables et des contraintes
    output_file.write(f"n = {n}\n")
    output_file.write(f"m = {int(n*(n-1)/2)}\n\n")

    # Écriture des variables pour les colonnes des reines
    for i in range(1, n + 1):
        output_file.write(f"c_{i} = {{{','.join(map(str, range(1, n + 1)))}}}\n")

    output_file.write("\n")

    # Génération des contraintes de différence de colonnes
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            constraint_name = f"C-c_{i}-c_{j}"
            # Génération de toutes les contraintes en une seule fois
            constraint_values = [(c_i, c_j) for c_i in range(1, n + 1) for c_j in range(1, n + 1) if c_j - c_i != j - i
                                 and c_i - c_j != j - i
                                 and c_i != c_j]

            output_file.write(f"{constraint_name} = {{{','.join(map(str, constraint_values))}}}\n")

    # Fermeture du fichier
    output_file.close()


def read_graph_dimacs(chemin_fichier):
    """
    Ouvre un fichier dans le format DIMACS représentant un graphe et crée un dictionnaire du graph
    :param chemin_fichier: Chemin vers le fichier DIMACS
    :return: Un tuple, le nombre de sommets, le nombre d'arrêtes et le dictionnaire qui représente le graphe
    """
    graphe = {}

    with open(chemin_fichier, 'r') as fichier:
        lignes = fichier.readlines()

        for ligne in lignes:
            # Ignorer les lignes de commentaire
            if ligne.startswith('c'):
                continue

            # Trouver la ligne définissant la structure du graphe
            if ligne.startswith('p'):
                _, _, nb_sommets, nb_aretes = ligne.split()
                nb_sommets, nb_aretes = int(nb_sommets), int(nb_aretes)
                break

        # Initialiser le dictionnaire avec des listes vides pour chaque sommet
        for i in range(1, nb_sommets + 1):
            graphe[i] = []

        # Parcourir les lignes d'arêtes et ajouter les voisins au dictionnaire
        for ligne in lignes:
            if ligne.startswith('e'):
                _, sommet1, sommet2 = ligne.split()
                sommet1, sommet2 = int(sommet1), int(sommet2)
                graphe[sommet1].append(sommet2)
                graphe[sommet2].append(sommet1)

    return nb_sommets, nb_aretes, graphe


def generate_graph_csp(graph, n, m, k, output_file):
    """
    Génère un CSP en .txt du problème coloration d'un graphe à partir d'un dictionnaire représentation un graphe
    et un nombre de couleurs.

    :param graph: Le dictionnaire représentant le graphe.
    :param n: Le nombre de sommets du graphe.
    :param m: Le nombre d'arrêtes du graphe.
    :param k: Le nombre de couleurs utilisable.
    :param output_file: Le chemin vers le fichier d'écriture du CSP.
    :return:
    """
    with open(output_file, 'w') as file:
        # Écriture du nombre de sommets (n) et d'arêtes (m)
        file.write(f'n = {n}\n')
        file.write(f'm = {2*m}\n\n')

        # Écriture des domaines des variables
        for node in range(1, n+1):
            file.write(f"{node} = {{{','.join(map(str, range(1, k+1)))}}}\n")

        file.write('\n')

        # Écriture des contraintes
        # Écriture des contraintes
        for node, neighbors in graph.items():
            for neighbor in neighbors:
                file.write(f'C-{node}-{neighbor} = {{')
                for i in range(1, k + 1):
                    for j in range(1, k + 1):
                        if i != j:
                            file.write(f'({i}, {j}), ')
                file.seek(file.tell() - 2)  # Supprimer la virgule et l'espace supplémentaires
                file.write('}\n')
