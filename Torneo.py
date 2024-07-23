def tcrz(dst, pareto, poblacion, bits, individuos):
    import numpy as np
    fil, col = np.shape(pareto)
    padre = np.zeros((5, 5))
    hijo1 = np.zeros((1, bits))
    hijo2 = np.zeros((1, bits))
    ap = np.zeros((3, 3))
    fpo, cpo = np.shape(poblacion)
    poblaux = poblacion*0
    for i in range(0, int((col-1)/2)):
        moneda1=np.random.randint(individuos)+1
        moneda2=np.random.randint(individuos)+1
        moneda3=np.random.randint(individuos)+1
        moneda4=np.random.randint(individuos)+1
        for ii in range(1, col):
            for jj in range(1, col):
                if pareto[ii, jj] == moneda1:
                    padre[1,1] = ii
                    padre[2,1] = jj
                if pareto[ii,jj] == moneda2:
                    padre[1,2]=ii
                    padre[2,2]=jj
                if pareto[ii, jj] == moneda3:
                    padre[1,3] = ii
                    padre[2,3] = jj
                if pareto[ii, jj] == moneda4:
                    padre[1,4] = ii
                    padre[2,4] = jj
        if padre[1,1]<padre[1,2]:
            ap[1,1]=padre[1,1]
            ap[2,1]=padre[2,1]
        elif padre[1,1]>padre[1,2]:
            ap[1,1]=padre[1,2]
            ap[2,1]=padre[2,2]
        else:
            if dst[int(padre[1,1]), int(padre[2,1])]>dst[int(padre[1,2]), int(padre[2,2])]:
                ap[1,1]=padre[1,1]
                ap[2,1]=padre[2,1]
            else:
                ap[1,1]=padre[1,2]
                ap[2,1]=padre[2,2]
        if padre[1,3]<padre[1,4]:
            ap[1,2]=padre[1,3]
            ap[2,2]=padre[2,3]
        elif padre[1,3]>padre[1,4]:
            ap[1,2]=padre[1,4]
            ap[2,2]=padre[2,4]
        else:
            if dst[int(padre[1,3]),int(padre[2,3])]>dst[int(padre[1,4]),int(padre[2,4])]:
                ap[1,2]=padre[1,3]
                ap[2,2]=padre[2,3]
            else:
                ap[1,2]=padre[1,4]
                ap[2,2]=padre[2,4]
        corte = np.random.randint(1, bits)
        for jj in range(0, bits):
            hijo1[0,jj] = poblacion[int(pareto[int(ap[1,1]), int(ap[2,1])]-1), jj]
            hijo2[0,jj] = poblacion[int(pareto[int(ap[1,2]), int(ap[2,2])]-1), jj]
            if jj >= corte:
                poblaux[i * 2 + 1, jj] = hijo1[0,jj]
                poblaux[i * 2, jj] = hijo2[0,jj]
            else:
                poblaux[i * 2 + 1, jj] = hijo2[0,jj]
                poblaux[i * 2, jj] = hijo1[0,jj]
    for i in range(int(fil/10)):
        Mutar = np.random.randint(0, col-1)
        for j in range(int(bits/2)):
            Bitmutado = np.random.randint(0, bits)
            if poblaux[Mutar, Bitmutado] == 0:
                poblaux[Mutar, Bitmutado] = 1
            else:
                poblaux[Mutar, Bitmutado] = 0
    R=np.concatenate((poblacion, poblaux))
    return R