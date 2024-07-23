def IMP(Results_Folder, individuos, pareto, RESPUESTA, NLL, RESPUESTApoblacion, RESP_inflexion, BarrasConPVs, Semilla, NombreArchivo, TipoDsimulacion, iteraciones):
    import numpy as np
    import pandas as pd

    Frente=0
    Bigger=0
    for i in range(1, individuos+1):
        if np.count_nonzero(pareto[i,:])!=0:
            Frente=Frente+1
        if np.count_nonzero(pareto[i,:])>Bigger:
            Bigger=np.count_nonzero(pareto[i,:])



    Power = np.zeros((Frente, Bigger))
    Dsq = np.zeros((Frente, Bigger))
    Power_inflexion = np.zeros((Frente, Bigger))
    Dsq_inflexion = np.zeros((Frente, Bigger))


    acum=0
    for i in range(1, Frente+1):
        for j in range(1, Bigger+1):
            if pareto[i,j]!=0:
                Power[i-1, j-1] = RESPUESTA[0, acum]
                Dsq[i-1, j-1] = RESPUESTA[1, acum]
                Power_inflexion[i-1, j-1] =  RESP_inflexion[0, acum]
                Dsq_inflexion[i-1, j-1] = RESP_inflexion[1, acum]
                acum = acum+1


    Power=-Power
    Power_inflexion=-Power_inflexion

    for i in range(Frente):
        for j in range(Bigger-1):
            for jj in range(1, Bigger):
                if Power[i, jj] > Power[i, j] and jj > j:
                    aux = Power[i, j]
                    Power[i, j] = Power[i, jj]
                    Power[i, jj] = aux

                    aux = Dsq[i, j]
                    Dsq[i, j] = Dsq[i, jj]
                    Dsq[i, jj] = aux

                    aux = Power_inflexion[i, j]
                    Power_inflexion[i, j] = Power_inflexion[i, jj]
                    Power_inflexion[i, jj] = aux

                    aux = Dsq_inflexion[i, j]
                    Dsq_inflexion[i, j] = Dsq_inflexion[i, jj]
                    Dsq_inflexion[i, jj] = aux
    Dsq = - Dsq

    PoblOrdenada=np.zeros((individuos, NLL))
    cont=0


    for i in range(Frente):
        for j in range(Bigger):
            Repetido = False
            for jj in range(individuos):
                if Power[i,j]==-RESPUESTA[0,jj] and Dsq[i,j]==-RESPUESTA[1,jj] and Repetido == False:
                    Vecaux = RESPUESTApoblacion[jj,:]
                    PoblOrdenada[cont,:]=Vecaux
                    cont = 1 + cont
                    Repetido = True

    Dsq = - Dsq


    Repuesta_Posicion_PVs = np.zeros((2*BarrasConPVs.shape[0], BarrasConPVs.shape[1]))

    for i in range(int(BarrasConPVs.shape[0]/2)):
        for ii in range(Dsq.shape[1]):
            if sum(BarrasConPVs[i * 2 + 1, :]) == Dsq[0, ii]:
                Repuesta_Posicion_PVs[ii * 2, :] = BarrasConPVs[i * 2, :]
                Repuesta_Posicion_PVs[ii * 2 +1, :] = BarrasConPVs[i * 2 + 1, :]


    ROP = 0
    for i in range(int(pareto.shape[1])):
        if pareto[1, i] != 0:
            ROP = int(pareto[1, i])

    pareto_Optimo = pareto[1, 1:pareto.shape[1]-1]
    Power_Optimo = Power[0, 0:ROP].round(2)
    HC_Optimo = Dsq[0, 0:ROP]
    Poblacion_Optimo = PoblOrdenada[0:ROP, :]
    Power_inflexion_Optimo = Power_inflexion[0, 0:ROP].round(2)
    HC_inflexion_Optimo = Dsq_inflexion[0, 0:ROP]
    Repuesta_Posicion_PVs_Optimo = Repuesta_Posicion_PVs[0:ROP*2, :]

    df1 = pd.DataFrame(Power_Optimo)
    df2 = pd.DataFrame(HC_Optimo)
    df3 = pd.DataFrame(Poblacion_Optimo)
    df4 = pd.DataFrame(Power_inflexion_Optimo)
    df5 = pd.DataFrame(HC_inflexion_Optimo)
    df6 = pd.DataFrame(Repuesta_Posicion_PVs_Optimo)

    NombreArchivo = TipoDsimulacion + '_Seed_' + str(Semilla) + '_It_' + str(iteraciones) + '_Ind_' + str(individuos) + '_' + NombreArchivo + '.xlsx'

    NombreAux = Results_Folder + "\\Reconfiguration\\"

    NombreArchivo = NombreAux + NombreArchivo

    writer = pd.ExcelWriter(NombreArchivo, engine='xlsxwriter')

    df1.to_excel(writer, sheet_name='Power')
    df2.to_excel(writer, sheet_name='HC')

    writer.close()


    return Power, Dsq

