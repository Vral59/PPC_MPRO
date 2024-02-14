def AC(variables, contraintes):

    def LocAC(a):
        nonlocal aTester
        nonlocal valeurs
        nonlocal c1
        nonlocal c2
        for b in variables[c2]:
            if (a, b) in valeurs:
                return True
        for indices, _ in contraintes.items(): # ajout des contraintes de la forme (c3, c1)
                if c1 == indices[0] and c2 not in indices:
                    aTester.append((indices[1], c1))
                elif c1 == indices[1] and c2 not in indices:
                    aTester.append((indices[0], c1))
        return False
    
    aTester = []
    for indices, _ in contraintes.items():
        aTester.append((indices[0], indices[1]))
        aTester.append((indices[1], indices[0]))
    while len(aTester) > 0:
        c1, c2 = aTester.pop(0)
        if (c1, c2) in contraintes.keys():
            valeurs = contraintes[(c1, c2)]
        else :
            valeurs = contraintes[(c2, c1)]
        variables[c1] = [a for a in variables[c1] if LocAC(a)]           
    return(variables, contraintes)