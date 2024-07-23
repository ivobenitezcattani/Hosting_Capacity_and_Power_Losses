def Crow(fitness, pareto):
    import numpy as np
    import functools
    fun, col = np.shape(fitness)
    f1min=fitness[0, 0]
    f1max=fitness[0, 0]
    f2min=fitness[1, 0]
    f2max=fitness[1, 0]
    cmin1 = 0
    cmin2 = 0
    cmax1 = 0
    cmax2 = 0
    for i in range(1, col):
        if fitness[0, i]<f1min:
            f1min = fitness[0, i]
            cmin1=i
        if fitness[0, i]>f1max:
            f1max = fitness[0, i]
            cmax1 = i
        if fitness[1, i]<f2min:
            f2min = fitness[1, i]
            cmin2 = i
        if fitness[1, i]>f2max:
            f2max = fitness[1, i]
            cmax2 = i
    fitpareto=np.zeros((col+1, col+1))
    for i in range(1, col+1):
        for j in range(1, col+1):
            if pareto[i, j]!=0:
                fitpareto[i, j] = fitness[0, int(pareto[i, j])-1]
    paretoaux = pareto
    for i in range(1, col+1):
        for j in range(1, col):
            jj = j
            while jj <= col - 1:
                jj = jj + 1
                if fitpareto[i, jj] < fitpareto[i, j] and pareto[i, jj]!=0:
                    aux = fitpareto[i, jj]
                    fitpareto[i, jj] = fitpareto[i, j]
                    fitpareto[i, j] = aux
                    aux = paretoaux[i, jj]
                    paretoaux[i, jj] = paretoaux[i, j]
                    paretoaux[i, j] = aux
    dst = np.zeros((col + 1, col + 1))
    for i in range(1, col+1):
        for j in range(1, col+1):
            if paretoaux[i, j]!=0 and j == 1:
                dst[i, j] = 10
            elif paretoaux[i, j]!=0 and j == col:
                dst[i, j] = 10
            elif paretoaux[i, j]!=0 and paretoaux[i, j + 1] == 0:
                dst[i, j] = 10
            elif paretoaux[i, j]!=0 and paretoaux[i, j + 1]!=0 and paretoaux[i, j + 1]!=0 and (fitness[1, int(cmax2)] - fitness[1, int(cmin2)]) != 0:
                dst[i, j] = (fitness[0, int(paretoaux[i, j + 1]-1)] - fitness[0, int(paretoaux[i, j - 1]-1)]) / (fitness[0, int(cmax1)] - fitness[0, int(cmin1)]) + (-fitness[1, int(paretoaux[i, j + 1]-1)] + fitness[1, int(paretoaux[i, j - 1]-1)]) / (fitness[1, int(cmax2)] - fitness[1, int(cmin2)])
    pareto = paretoaux
    for i in range(1, col+1):
        for j in range(1, col):
            jj = j
            while jj <= col - 1:
                jj = jj + 1
                if dst[i, jj] > dst[i, j] and dst[i, jj]!=0:
                    aux = paretoaux[i, jj]
                    paretoaux[i, jj] = paretoaux[i, j]
                    paretoaux[i, j] = aux
                    aux = dst[i, jj]
                    dst[i, jj] = dst[i, j]
                    dst[i, j] = aux
    pareto = paretoaux
    return dst, pareto