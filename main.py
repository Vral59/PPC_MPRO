import readcsp
import geninstance


def main():
    # Exemple d'utilisation de la lecture d'un fichier csp
    nom_fichier_csp = 'instance/exemple_csp.txt'
    n, m, variables, contraintes = readcsp.lire_fichier_csp(nom_fichier_csp)

    if n is not None and m is not None and variables is not None and contraintes is not None:
        print("Nombre de variables:", n)
        print("Nombre de contraintes:", m)
        print("\nVariables:")
        for nom, domaine in variables.items():
            print(f"{nom}: {domaine}")

        print("\nContraintes:")
        for indices, valeurs in contraintes.items():
            print(f"C-{indices[0]}-{indices[1]}: {valeurs}")

    # Création du csp binaire pour le problème des n reines avec n = 4
    geninstance.generate_queens_csp(4, "instance/queens_csp.txt")


if __name__ == "__main__":
    main()
