from typing import Dict, List, Set, Tuple


def ac3(variables: Dict[str, List[int]], contraintes: Dict[Tuple[str, str], List[Tuple[int, int]]]) -> Tuple[
    Dict[str, List[int]], Dict[Tuple[str, str], List[Tuple[int, int]]]]:
    """
    Applique l'Arc-Consistency à un ensemble de variables et de contraintes.

    :param variables: Un dictionnaire où les clés sont les noms des variables et les valeurs sont des listes de domaines possibles.
    :param contraintes: Un dictionnaire où les clés sont des paires de variables et les valeurs sont des listes de valeurs autorisées.
    :return: Un tuple contenant les variables mises à jour et les contraintes mises à jour après l'application de l'Arc-Consistency.
    """
    variables_copy = {key: value.copy() for key, value in variables.items()}

    def LocAC(a: int) -> bool:
        """
        Fonction interne pour vérifier la consistance locale pour une valeur donnée.

        :param a: Valeur à tester pour la consistance locale.
        :return: True si la valeur est consistante, False sinon.
        """
        nonlocal aTester, valeurs, c1, c2, ajout_contraintes
        for b in variables_copy[c2]:
            if (a, b) in valeurs:
                return True
        ajout_contraintes = True
        return False

    aTester = []
    for indices, _ in contraintes.items():
        aTester.append((indices[0], indices[1]))
        aTester.append((indices[1], indices[0]))

    while len(aTester) > 0:
        c1, c2 = aTester.pop(0)
        if (c1, c2) in contraintes.keys():
            valeurs = contraintes[(c1, c2)]
        else:
            valeurs = contraintes[(c2, c1)]
        ajout_contraintes = False
        variables_copy[c1] = [a for a in variables_copy[c1] if LocAC(a)]
        if ajout_contraintes:
            for indices, _ in contraintes.items():
                if c1 == indices[0] and c2 not in indices:
                    aTester.append((indices[1], c1))
                elif c1 == indices[1] and c2 not in indices:
                    aTester.append((indices[0], c1))

    return variables_copy, contraintes


def _initAC4(variables: Dict[str, List[int]], contraintes: Dict[Tuple[str, str], List[Tuple[int, int]]]) -> Tuple[
    Set[Tuple[str, int]], Dict[Tuple[str, int], Set[Tuple[str, int]]]]:
    """
    Initialise l'Arc-Consistency 4 (AC4) avec une file Q et un dictionnaire S.

    :param variables: Un dictionnaire où les clés sont les noms des variables et les valeurs sont des listes de domaines possibles.
    :param contraintes: Un dictionnaire où les clés sont des paires de variables et les valeurs sont des listes de valeurs autorisées.
    :return: Un tuple contenant la file Q et le dictionnaire S initialisés pour l'Arc-Consistency 4.
    """

    Q = set()
    S = {}

    for c, valeurs in contraintes.items():
        x, y = c
        for a in variables[x]:
            total = 0
            for b in variables[y]:
                if (a, b) in valeurs:
                    total += 1
                    if (y, b) not in S:
                        S[(y, b)] = set()
                    S[(y, b)].add((x, a))
            if total == 0:
                variables[x] = [val for val in variables[x] if val != a]
                Q.add((x, a))

    return Q, S


def ac4(variables: Dict[str, List[int]], contraintes: Dict[Tuple[str, str], List[Tuple[int, int]]]) -> Tuple[
    Dict[str, List[int]], Dict[Tuple[str, str], List[Tuple[int, int]]]]:
    """
    Applique l'Arc-Consistency 4 (AC4) à un ensemble de variables et de contraintes.

    :param variables: Un dictionnaire où les clés sont les noms des variables et les valeurs sont des listes de domaines possibles.
    :param contraintes: Un dictionnaire où les clés sont des paires de variables et les valeurs sont des listes de valeurs autorisées.
    :return: Un tuple contenant les variables mises à jour et les contraintes mises à jour après l'application de l'Arc-Consistency 4.
    """
    variables_copy = {key: value.copy() for key, value in variables.items()}
    Q, S = _initAC4(variables_copy, contraintes)

    while Q:
        y, b = Q.pop()
        for x, a in S.get((y, b), set()):
            if (x, a) in Q:
                Q.remove((x, a))
            for x_a, y_b in S.items():
                if (x, a) in y_b:
                    y_b.remove((x, a))
                    if len(y_b) == 0 and a in variables_copy[x]:
                        variables_copy[x].remove(a)
                        Q.add((x, a))

    return variables_copy, contraintes
