import readcsp
import geninstance
import backtrack
import backtrack_queens
import backtrack_color
import AC
import time


def test_nqueens():
    """
    Fonction de démonstration du CSP des nqueens.
    """
    # Création du csp binaire pour le problème des n reines avec n = 4
    n = 45
    nom_fichier_csp = "instance/queens_csp.txt"
    # Création d'un CSP
    #geninstance.generate_queens_csp(n, nom_fichier_csp)
    # Lecture du CSP
    n, m, variables, contraintes = readcsp.lire_fichier_csp(nom_fichier_csp)
    print("---------Debut resolution-----")

    # Symetries
    # geninstance.add_c1_smaller_c2(variables, contraintes, '1', str(n))

    # Résolutions
    start_time = time.time()
    resultat = backtrack.backtrack(variables, contraintes, True, False, False, "smallest_domain", "smallest")
    end_time = time.time()
    if resultat is None:
        print("Pas de solution possible pour ce problème de reines")
    else:
        print("Résultat problèmes ", str(n), " reines : ", resultat, "\n")
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
    # Lecture du DIMACS
    nb_sommets, nb_aretes, graph = geninstance.read_graph_dimacs("instance/DIMACS Graphs/huck.col")
    nom_fichier_csp_graph = 'instance/exemple_csp_graph.txt'
    # Creation du CSP à partir du DIMACS
    geninstance.generate_graph_csp(graph, nb_sommets, nb_aretes, 11, nom_fichier_csp_graph)
    n, m, variables, contraintes = readcsp.lire_fichier_csp(nom_fichier_csp_graph)
    # Application de l'algorithme d'AC4
    variables, contraintes = AC.AC4(variables, contraintes)
    # Résolution du problème
    start_time = time.time()
    resultat = backtrack.backtrack(variables, contraintes, False, False, True, "random", "smallest")
    end_time = time.time()
    if resultat is None:
        print("Pas de solution possible pour ce problème de coloration")
    else:
        print("Résultat problèmes de coloration: ", resultat, "\n")
    print("Temps de calcul : ", end_time - start_time)


def main():
    # Test nqueens :
    #test_nqueens()
    # Test carrosserie
    #test_carrosserie()
    # Test coloration
    test_coloration()


if __name__ == "__main__":
    main()
