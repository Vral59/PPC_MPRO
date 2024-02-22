from typing import Any


def read_csp_file(file_path: str) -> tuple[None, None, None, None] | \
                                     tuple[int, int, dict[str, Any], dict[tuple[str, ...], Any]]:
    """
    Lit un fichier CSP dans un format spécifique et stocke les données.

    :param file_path: Chemin vers le fichier .txt.
    :return: Un tuple contenant le nombre de variables, le nombre de contraintes, un dictionnaire de variables et de
            leurs domaines, et un dictionnaire de tuples de variables et de valeurs.
    """
    variables = {}
    constraints = {}

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

            if len(lines) < 4:
                raise ValueError("Le fichier ne contient pas suffisamment de lignes.")

            n = int(lines[0].strip().split('=')[1])
            m = int(lines[1].strip().split('=')[1])

            current_line = 3  # Skip the first two lines and the empty line
            for i in range(n):
                if current_line >= len(lines):
                    raise ValueError("Nombre insuffisant de lignes pour les variables.")

                line = lines[current_line].strip().split('=')
                if len(line) == 2:
                    variable_name = line[0].strip()
                    domain = eval(line[1].strip())  # Using eval to handle sets
                    variables[variable_name] = domain
                    current_line += 1
                else:
                    raise ValueError("Format invalide pour la définition d'une variable.")

            current_line += 1  # Skip the empty line after variables

            for j in range(m):
                if current_line >= len(lines):
                    raise ValueError("Nombre insuffisant de lignes pour les contraintes.")

                line = lines[current_line].strip().split('=')
                if len(line) == 2:
                    concerned_variables = tuple(map(str, line[0].strip().split('-')[1:]))
                    valid_tuples = eval(line[1].strip())
                    constraints[concerned_variables] = valid_tuples
                    current_line += 1
                else:
                    raise ValueError("Format invalide pour la définition d'une contrainte.")

    except (IOError, ValueError, SyntaxError) as e:
        print(f"Erreur lors de la lecture du fichier : {str(e)}")
        return None, None, None, None

    return n, m, variables, constraints
