import readcsp
import geninstance
import backtrack
import backtrack_queens
import AC
import time


def test_nqueens():
    """
    Fonction de démonstration du CSP des nqueens.
    """
    # Création du csp binaire pour le problème des n reines avec n = 4
    nom_fichier_csp = "instance/queens_csp.txt"
    # Création d'un CSP
    geninstance.generate_queens_csp(50, nom_fichier_csp)
    # Lecture du CSP
    n, m, variables, contraintes = readcsp.lire_fichier_csp(nom_fichier_csp)

    # Symetries
    #print("contraintes[x1, x2] = ", contraintes[('c_1', 'c_' + str(n))], "\n")
    geninstance.add_c1_smaller_c2(variables, contraintes, 'c_1', 'c_' + str(n))
    #print("contraintes [x1, x2]= ", contraintes[('c_1', 'c_' + str(n))])

    # Résolutions
    start_time = time.time()
    resultat = backtrack_queens.backtrack(variables, contraintes, True, "smallest_domain")
    end_time = time.time()
    if resultat is None:
        print("Pas de solution possible pour ce problème de reines")
    else:
        print("Résultat problèmes 12 reines : ", resultat, "\n")
        print("Variables : ", variables)
        print("Temps de calcul : ", end_time - start_time)


def test_carrosserie():
    """
    Fonction de démonstration de l'AC3.
    """
    nom_fichier_csp = "instance/carrosserie.txt"
    n, m, variables, contraintes = readcsp.lire_fichier_csp(nom_fichier_csp)
    print("Variables : ", variables)
    print("Contraintes : ", contraintes, "\n")
    variables, contraintes = AC.AC(variables, contraintes)
    print("Résultat problème carrosserie : ")
    print("Variables : ", variables)
    print("Contraintes : ", contraintes)
    resultat = backtrack.backtrack(variables, contraintes)
    if resultat is None:
        print("Pas de solution possible pour ce problème de carrosserie")
    else:
        print("Résultat problèmes carrosserie : ", resultat, "\n")


def test_coloration():
    """
    Fonction de démonstration du CSP de coloration d'un graphe.
    """
    nb_sommets, nb_aretes, graph = geninstance.read_graph_dimacs("instance/DIMACS Graphs/light_graph.col")
    print(graph)
    nom_fichier_csp_graph = 'instance/exemple_csp_graph.txt'
    geninstance.generate_graph_csp(graph, nb_sommets, nb_aretes, 2, nom_fichier_csp_graph)
    n, m, variables, contraintes = readcsp.lire_fichier_csp(nom_fichier_csp_graph)
    start_time = time.time()
    resultat = backtrack.backtrack(variables, contraintes)
    end_time = time.time()
    if resultat is None:
        print("Pas de solution possible pour ce problème de coloration")
    else:
        print("Résultat problèmes de coloration: ", resultat, "\n")
    print("Temps de calcul : ", end_time - start_time)


def main():
    # Exemple d'utilisation de la lecture d'un fichier csp
    nom_fichier_csp = 'instance/exemple_csp.txt'
    n, m, variables, contraintes = readcsp.lire_fichier_csp(nom_fichier_csp)

    if n is not None and m is not None and variables is not None and contraintes is not None:
        print("Exemple de lecture d'un CSP avec le fichier fichier : ", nom_fichier_csp)
        print("Nombre de variables:", n)
        print("Nombre de contraintes:", m)
        print("\nVariables:")
        for nom, domaine in variables.items():
            print(f"{nom}: {domaine}")

        print("\nContraintes:")
        for indices, valeurs in contraintes.items():
            print(f"C-{indices[0]}-{indices[1]}: {valeurs}")
        print("")

    resultat = backtrack.backtrack(variables, contraintes)
    print("Résultat problème du cours : ", resultat, "\n")

    # Test nqueens :
    test_nqueens()
    # Test carrosserie
    #test_carrosserie()
    # Test coloration
    #test_coloration()


if __name__ == "__main__":
    main()
