def BarrasconPV(objeto):
    import numpy as np
    NombreCargas = objeto.dssLoads.AllNames
    objeto.dssCircuit.setActiveElement("Load." + objeto.dssLoads.Name)
    NombreBarrasCargas = np.zeros((len(NombreCargas)))
    NroFasesBarras = np.zeros((3, len(NombreCargas)))
    NombreFases = np.zeros((4, len(NombreCargas)))
    objeto.dssLoads.First
    for j in range(len(NombreCargas)):
        variable = objeto.dssCktElement.BusNames
        variable = variable[0].split(".")
        NombreBarrasCargas[j] = variable[0]
        NroFasesBarras[0, j] = objeto.dssCktElement.NumPhases
        NroFasesBarras[1, j] = objeto.dssLoads.IsDelta
        NroFasesBarras[2, j] = objeto.dssLoads.kva
        variable2 = objeto.dssCktElement.NodeOrder
        NombreFases[0, j] = variable[0]
        NombreFases[1, j] = variable2[0]
        if len(variable2) == 2:
            NombreFases[2, j] = variable2[1]
        elif len(variable2) == 3 or len(variable2) == 4:
            NombreFases[2, j] = variable2[1]
            NombreFases[3, j] = variable2[2]
        objeto.dssLoads.Next
    for j in range(len(NombreCargas)):
        CONBARRAS = 0
        for jj in range(len(NombreCargas)):
            if NombreBarrasCargas[j] == NombreBarrasCargas[jj] and NroFasesBarras[0, j] < 3:
                CONBARRAS = CONBARRAS + 1
                NroFasesBarras[0, j] = CONBARRAS
    Load_fases = np.zeros((4, len(NombreCargas)))
    col = 0
    for j in range(len(NombreCargas)):
        BarraRep = 0
        for jj in range(j, -1, -1):
            if NombreFases[0, j] == Load_fases[0, jj]:
                BarraRep = 1
                for i in range(1, 4):
                    NodoRep = 0
                    for ii in range(1, 4):
                        if NombreFases[i, j] == Load_fases[ii, jj] and NombreFases[i, j] != 0:
                            NodoRep = 1
                    if NodoRep == 0:
                        YaEncontroDifzero = 0
                        for iii in range(1, 4):
                            if Load_fases[iii, jj] == 0 and YaEncontroDifzero == 0:
                                Load_fases[iii, jj] = NombreFases[i, j]
                                YaEncontroDifzero = 1
        if BarraRep == 0:
            Load_fases[:, col] = NombreFases[:, j]
            col = col + 1
    NBCaux = np.zeros((4, (len(NombreCargas))))
    jjj = 0
    for j in range(len(NombreCargas)):
        RepiteBarras = 0
        for jj in range(j, len(NombreCargas)):
            if NombreBarrasCargas[j] == NombreBarrasCargas[jj] and j != jj:
                if RepiteBarras == 0 and NBCaux[3, jjj] == 0:
                    NBCaux[3, jjj] = NroFasesBarras[2, j] + NroFasesBarras[2, jj]
                elif RepiteBarras == 1:
                    NBCaux[3, jjj] = NroFasesBarras[2, jj] + NBCaux[3, jjj]
                RepiteBarras = 1
        if RepiteBarras == 0:
            NBCaux[0, jjj] = NombreBarrasCargas[j]
            NBCaux[1, jjj] = NroFasesBarras[0, j]
            NBCaux[2, jjj] = NroFasesBarras[1, j]
            if NBCaux[3, jjj] == 0:
                NBCaux[3, jjj] = NroFasesBarras[2, j]
            jjj = jjj + 1
    NbLoad = jjj
    NBC = np.zeros((4, NbLoad))
    for j in range(NbLoad):
        NBC[0, j] = NBCaux[0, j]
        NBC[1, j] = NBCaux[1, j]
        NBC[2, j] = NBCaux[2, j]
        NBC[3, j] = NBCaux[3, j]
    return NBC, Load_fases, NbLoad