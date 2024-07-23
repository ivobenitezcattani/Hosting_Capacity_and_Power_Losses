def Pr(NB, difx, dify, peso, serie, BusWeight, NLL):
    import numpy as np
    INF = 9999999
    pred = np.zeros((NB))
    G = np.zeros((NB, NB))
    N = NB
    for i in range(serie):
        G[int(difx[i]), int(dify[i])] = peso[i]
        G[int(dify[i]), int(difx[i])] = peso[i]
    selected_node = np.zeros(NB)
    pred = np.zeros((3, NB-1))
    salto = 0
    no_edge = 0
    selected_node[0] = True
    while (no_edge < N - 1):
        minimum = INF
        a = 0
        b = 0
        for m in range(N):
            if selected_node[m]:
                for n in range(N):
                    if ((not selected_node[n]) and G[m][n]):
                        if minimum > G[m][n]:
                            minimum = G[m][n]
                            a = m
                            b = n
                            aux = G[m][n]
        pred[0, salto] = a
        pred[1, salto] = b
        pred[2, salto] = aux
        salto= salto + 1
        selected_node[b] = True
        no_edge += 1
    key= np.zeros(NLL)
    for jj in range(NB-1):
        for z in range(NLL):
            if (pred[0, jj] == BusWeight[0, z] and pred[1, jj] == BusWeight[1, z]) or (pred[0, jj] == BusWeight[1, z] and pred[1, jj] == BusWeight[0, z]):
                key[z] = 1
    return key