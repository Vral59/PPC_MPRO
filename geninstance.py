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
