import readcsp
import geninstance
import backtrack
import AC

def main():
    # Exemple d'utilisation de la lecture d'un fichier csp
    nom_fichier_csp = 'instance/exemple_csp.txt'
    n, m, variables, contraintes = readcsp.lire_fichier_csp(nom_fichier_csp)

    if n is not None and m is not None and variables is not None and contraintes is not None:
        print("Exemple de lectture d'un CSP avec le fichier fichier : ", nom_fichier_csp)
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
    print("Résultat problème du cours : ",resultat, "\n")

    # Création du csp binaire pour le problème des n reines avec n = 4
    nom_fichier_csp = "instance/queens_csp.txt"
    # Création d'un CSP
    geninstance.generate_queens_csp(4, nom_fichier_csp)
    # Lecture du CSP
    n, m, variables, contraintes = readcsp.lire_fichier_csp(nom_fichier_csp)
    # Résolutions
    resultat = backtrack.backtrack(variables, contraintes)
    print("Résultat problèmes 4 reines : ", resultat, "\n")

    nom_fichier_csp = "instance/carrosserie.txt"
    n, m, variables, contraintes = readcsp.lire_fichier_csp(nom_fichier_csp)
    print("Variables : ", variables)
    print("Contraintes : ", contraintes, "\n")
    variables, contraintes = AC.AC(variables, contraintes)
    print("Résultat problème carrosserie : ")
    print("Variables : ", variables)
    print("Contraintes : ", contraintes)
if __name__ == "__main__":
    main()
