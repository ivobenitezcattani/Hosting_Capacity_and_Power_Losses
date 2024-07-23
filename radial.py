def rad(poblacion, BusWeight, NB, NLL, individuos, serie):
    import numpy as np
    import random
    difx = np.zeros((serie))
    dify = np.zeros((serie))
    peso = np.zeros((serie))
    for i in range(serie):
        difx[i] = BusWeight[0, i]
        dify[i] = BusWeight[1, i]
        peso[i] = 0.01
    key = np.zeros((individuos, NLL))
    for i in range(individuos):
        for j in range(NLL):
            difx[j] = BusWeight[0, j]
            dify[j] = BusWeight[1, j]
            if poblacion[i, j] == 1:
                peso[j] = 10
            elif poblacion[i, j] == 0:
                peso[j] = 90 + random.randint(0, 10)
        from Prim import Pr
        key = Pr(NB, difx, dify, peso, serie, BusWeight, NLL)
        poblacion[i, :] = key[:]
    return poblacion