def AC(variables, contraintes):

    def LocAC(a):
        nonlocal aTester
        nonlocal valeurs
        nonlocal c1
        nonlocal c2
        nonlocal ajout_contraintes
        for b in variables[c2]:
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
        else :
            valeurs = contraintes[(c2, c1)]
        ajout_contraintes = False
        variables[c1] = [a for a in variables[c1] if LocAC(a)]  
        if ajout_contraintes:
            for indices, _ in contraintes.items(): # ajout des contraintes de la forme (c3, c1)
                if c1 == indices[0] and c2 not in indices:
                    aTester.append((indices[1], c1))
                elif c1 == indices[1] and c2 not in indices:
                    aTester.append((indices[0], c1))         
    return(variables, contraintes)


def initAC4(variables, contraintes):
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


def AC4(variables, contraintes):
    Q, S = initAC4(variables, contraintes)

    while Q:
        y, b = Q.pop()
        for x, a in S.get((y, b), set()):
            if (x, a) in Q:
                Q.remove((x, a))
            for x_a, y_b in S.items():
                if (x, a) in y_b:
                    y_b.remove((x, a))
                    if len(y_b) == 0 and a in variables[x]:
                        variables[x].remove(a)
                        Q.add((x, a))

    return variables, contraintes
