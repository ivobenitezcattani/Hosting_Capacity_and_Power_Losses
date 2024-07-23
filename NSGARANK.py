def RANK(fitness):
    import numpy as np
    fun, col = np.shape(fitness)
    fitaux = np.zeros((fun+1, col+1))
    for i in range(fun):
        for j in range(col):
            fitaux[i+1, j+1]=fitness[i, j]
    fitness=fitaux
    r = col
    rr = r - 1
    vdom = np.zeros(r+1)
    perdio = np.zeros((r+1, r+1))
    domi = np.zeros((r+1, r+1, fun+1))
    pareto = np.zeros((r+1, r+1))
    sop = np.zeros(r+1)
    for i in range(1, r+1):
        vdom[i] = 0
        for j in range(1, r+1):
            perdio[i, j] = 0
            pareto[i, j] = 0
            for ii in range(1, fun+1):
                domi[i, j, ii] = 0
    while r != 1:
        while rr != 0:
            for i in range(1, fun+1):
                if fitness[i, r] < fitness[i, rr]:
                    domi[r, rr, i] = 1
                elif fitness[i, r] > fitness[i, rr]:
                    domi[rr, r, i] = 1
                elif fitness[i, r] == fitness[i, rr]:
                    domi[r, rr, i] = 2
                    domi[rr, r, i] = 2
            rr = rr - 1
        r = r - 1
        rr = r - 1
    for r in range(1, col+1):
        for rr in range(1, col+1):
            for i in range(1, fun+1):
                if domi[r, rr, i] == 1:
                    perdio[r, rr] = 1
    aux = 1
    for i in range(1, col+1):
        for j in range(1, col+1):
            if i == 1:
                pareto[i, j] = aux
                aux = aux + 1
            else:
                pareto[i, j] = 0
    salto = 1
    while salto <= col - 1:
        cont = 1
        while cont <= col and pareto[salto, cont] != 0:
            aux = pareto[salto, cont]
            vdom[:]=0
            for j in range(1, col+1):
                if pareto[salto, j]!=0:
                    if perdio[int(pareto[salto, j]), int(aux)] < perdio[int(aux), int(pareto[salto, j])]:
                        vdom[j] = 3
                    elif perdio[int(pareto[salto, j]), int(aux)] > perdio[int(aux), int(pareto[salto, j])]:
                        vdom[j] = 1
                    else:
                        vdom[j] = 2
            pasa = 0
            for ii in range(1, col+1):
                if vdom[ii] == 3:
                    pasa = 3
            if pasa == 0:
                for ii in range(1, col+1):
                    if vdom[ii] == 2:
                        pasa = 2
                if pasa == 2:
                    for ii in range(1, col+1):
                        if vdom[ii] == 1:
                            pasa = 4
                if pasa == 0:
                    pasa = 1
            if pasa == 3:
                out = 0
                for ii in range(1, col+1):
                    if pareto[salto + 1, ii] == 0 and out == 0:
                        pareto[salto + 1, ii] = pareto[salto, cont]
                        out = 1
                for ii in range(cont, col):
                    pareto[salto, ii] = pareto[salto, ii + 1]
                pareto[salto, col] = 0
                cont = cont - 1
            elif pasa == 2:
                Nohacenada=0
            elif pasa == 4:
                out = 0
                for jj in range(1, col+1):
                    if pareto[salto + 1, jj] == 0 and out == 0:
                        stt = jj
                        out = 1
                jj = stt
                for ii in range(1, col+1):
                    if vdom[ii] == 1:
                        pareto[salto + 1, jj] = pareto[salto, ii]
                        jj = jj + 1
                        pareto[salto, ii] = 0
                cont = 0
                jj = 1
                sop[:] = pareto[salto, :]
                pareto[salto, :]=0
                for ii in range(1, col+1):
                    if sop[ii]!=0:
                        pareto[salto, jj] = sop[ii]
                        jj = jj + 1
            elif pasa == 1:
                out = 0
                for jj in range(1, col+1):
                    if pareto[salto + 1, jj] == 0 and out == 0:
                        pareto[salto + 1, jj] = sop[ii]
                        stt = jj
                        out = 1
                for ii in range(1, col+1):
                    if ii!=cont:
                        pareto[salto + 1, stt] = sop[ii]
                        stt = stt + 1
                pareto[salto, :] = 0
                pareto[salto, :] = pareto[salto, cont]
                cont = 0
                cont = col
            cont = cont + 1
            if cont < col and pareto[salto, cont] == 0:
                cont = col + 1
        salto = salto + 1
    return pareto