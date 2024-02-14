def AC(variables, contraintes):
    aTester = []
    for indices, _ in contraintes.items():
        aTester.append((indices[0], indices[1]))
        aTester.append((indices[1], indices[0]))
    while len(aTester) > 0:
        print("a tester = ", aTester)
        c1, c2 = aTester.pop(0)
        if (c1, c2) in contraintes.keys():
            valeurs = contraintes[(c1, c2)]
        else :
            valeurs = contraintes[(c2, c1)]
        for valeur in variables[c1]:
            if not any((valeur, v2) in valeurs for v2 in variables[c2]):
                print("valeur ", valeur, "pour la contrainte ", c1, c2, "n'est pas possible")
                print("variables[c1] = ", variables[c1])
                variables[c1].remove(valeur)
                print("variables[c1] = ", variables[c1])
                for indices, valeurs in contraintes.items():
                    if c1 == indices[0] and c2 not in indices:
                        aTester.append((indices[1], c1))
                    elif c1 == indices[1] and c2 not in indices:
                        aTester.append((indices[0], c1))
    return(variables, contraintes)