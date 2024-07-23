import win32com.client
from pylab import *
import random

class DSS():

    def __init__(self, llama_DSS):
        self.llama_DSS = llama_DSS
        self.dssObj = win32com.client.Dispatch("OpenDSSEngine.DSS")
        if self.dssObj.Start(0) == False:
            print("Problems starting OpenDSS")
        else:
            self.dssText = self.dssObj.Text
            self.dssCircuit = self.dssObj.ActiveCircuit
            self.dssSolution = self.dssCircuit.Solution
            self.dssCktElement = self.dssCircuit.ActiveCktElement
            self.dssBus = self.dssCircuit.ActiveBus
            self.dssLines = self.dssCircuit.Lines
            self.dssSwitch = self.dssCircuit.SwtControls
            self.dssTransformers = self.dssCircuit.Transformers
            self.dssRegControls = self.dssCircuit.RegControls
            self.dssCapacitors = self.dssCircuit.Capacitors
            self.dssLoads = self.dssCircuit.Loads
            self.dssPV = self.dssCircuit.PVSystems
            self.dssCtrlQueue = self.dssCircuit.CtrlQueue
            self.dssSolution = self.dssCircuit.Solution
            self.dssTopology = self.dssCircuit.Topology

    def compilar_DSS(self):
        self.dssObj.ClearAll()
        self.dssText.Command = "compile " + self.llama_DSS

    def RunOpenDSS(self):
        self.dssSolution.Solve()
    def DSSBusnames(self):
        Busnames = self.dssCircuit.AllBusNames
        return array(Busnames)
    def Lines(self):
        ALLLines = self.dssLines.AllNames
        return array(ALLLines)
    def buses(self):
        barras = self.dssCktElement.BusNames
        barra1 = barras[0]
        barra2 = barras[1]
        return barra1, barra2

            # =============================================================================================
            # ============ Below, specify the range of the seeds (from lower to higher limit). ============
            # =============================================================================================

Seed_Range = [0, 1]                                   # TODO             <<============  Enter the range of the seeds here.

CantidadIter = Seed_Range[0]

if __name__ == "__main__":

    while CantidadIter <= Seed_Range[1]:

            # =============================================================================================
            # =================== Below, select one strategy to use in the simulations. ===================
            # =============================================================================================

        # TipoDsimulacion = "ReconfLocked"                  # TODO               <<============   Network Reconfiguration
        # TipoDsimulacion = "ConRegSinReconf"               # TODO              <<============   OLTC Switching
        # TipoDsimulacion = "BCapLocked"                    # TODO              <<============   Capacitor Switching
        # TipoDsimulacion = "PVLocked"                      # TODO              <<============   Volt-VAR Control Settings
        TipoDsimulacion = "TotalOpt"                      # TODO              <<============   Combination of all strategies


            # ==========================================================================================================
            # ====== Below, specify the number of individuals and the number of iterations for each simulation. ========
            # ==========================================================================================================

        individuos = 6                      # TODO              <<============  Enter the number of individuals in each population.
        iteraciones = 2                     # TODO              <<============  Enter the number of iterations for each simulation.


            # ==========================================================================================================
            # ======================= Below, copy the path of the system modeled in OpenDSS. ===========================
            # ==========================================================================================================

        objeto = DSS(r"C:\Users\ACER\Desktop\Hosting_Capacity_and_Power_Losses\Modified_IEEE123nodetestSystem\IEEE123Master.dss")


            # ==========================================================================================================
            # ================= Below, copy the path of the folder where the results will be stored ====================
            # ==========================================================================================================

        Results_Folder = r"C:\Users\ACER\Desktop\Hosting_Capacity_and_Power_Losses\Outcomes"


        objeto.compilar_DSS()
        objeto.RunOpenDSS()
        SistemaConPv = "SI"
        Semilla = CantidadIter
        Busnames = objeto.DSSBusnames()
        from datetime import datetime
        start_time = datetime.now()

        def Vaux_BusVoltaux(Vaux, Busnames, AllNodeNames):
            BusVoltaux = np.zeros(len(Busnames) * 6)
            jaux = 0
            jNames = 0
            sale = 0
            for j in range(len(Busnames)):
                jaux = j * 6

                for jj in range(3):
                    if jNames < len(AllNodeNames):
                        RefB, Refn = AllNodeNames[jNames].split(".")
                    else:
                        sale = 1
                    if Busnames[j] == RefB and Refn == '1' and sale == 0:
                        BusVoltaux[jaux + 0] = Vaux[jNames * 2]
                        BusVoltaux[jaux + 1] = Vaux[jNames * 2 + 1]
                        jNames = jNames + 1
                    elif Busnames[j] == RefB and Refn == '2' and sale == 0:
                        BusVoltaux[jaux + 2] = Vaux[jNames * 2]
                        BusVoltaux[jaux + 3] = Vaux[jNames * 2 + 1]
                        jNames = jNames + 1
                    elif Busnames[j] == RefB and Refn == '3' and sale == 0:
                        BusVoltaux[jaux + 4] = Vaux[jNames * 2]
                        BusVoltaux[jaux + 5] = Vaux[jNames * 2 + 1]
                        jNames = jNames + 1

            Vaux = BusVoltaux
            return Vaux
        def VecToNum(RegBinarySeparado):
            signo = RegBinarySeparado[:1]
            RegBinarySeparado = RegBinarySeparado.astype(int)
            listadelvector = RegBinarySeparado[1:6]
            VectorReg = [str(i) for i in listadelvector]
            Unificado = int("".join(VectorReg))
            Decimal = int((str(Unificado)), 2)
            if Decimal > 16:
                Decimal = Decimal - 16
                listadelvector = bin(Decimal).replace("0b", "")
                zerosToAdd = '00000'
                zerosToAdd = zerosToAdd[0:5 - len(listadelvector)]
                listadelvector = zerosToAdd + listadelvector
                listadelvector = [int(x) for x in str(listadelvector)]
                listadelvector = np.array(listadelvector)
            if signo == 1:
                Decimal = -Decimal
            Unificado = signo.tolist() + listadelvector.tolist()
            return Unificado, Decimal

        def posicionRep(Vec1, ValBuscar):
            posicionElemento = -1
            for j in range(len(Vec1)):
                if str(int(ValBuscar)) == str(int(Vec1[j])):
                    posicionElemento = j
            return posicionElemento

        NB = len(Busnames)
        ApunN=[0] * NB

        for i in range(NB):
            ApunN[i] = i

        ALLLines = objeto.Lines()
        NLin = len(ALLLines)

        import numpy as np
        BusL = np.zeros((NLin*2, 1), dtype=str)
        BusL = BusL.tolist()
        BusLnum = np.zeros((NLin*2))
        BusSWnum = np.zeros((NLin*2))
        Elemento=objeto.dssLines.First
        NameLinSw = ["" for x in range(objeto.dssSwitch.Count)]
        jj=0
        LineLengths = np.zeros(NLin)
        for i in range(NLin):
            ii = i * 2
            a=objeto.dssLines.Bus1
            b=objeto.dssLines.Bus2
            LineLengths[i] = objeto.dssLines.Length
            a=a.split(".")
            a = a[0]
            b=b.split(".")
            b = b[0]
            BusL[ii][0] = (a)
            BusL[ii+1][0] = (b)
            SControl=objeto.dssCktElement.HasSwitchControl
            for j in range(NB):
                if BusL[ii][0] == Busnames[j]:
                    BusLnum[ii] = ApunN[j]
                    if SControl == 1:
                        BusSWnum[ii] = ApunN[j]

                        NameLinSw[jj] =  objeto.dssLines.Name
                        jj=jj+1
                    else:
                        BusSWnum[ii] = -100
                if BusL[ii+1][0] == Busnames[j]:
                    BusLnum[ii + 1] = ApunN[j]
                    if SControl == 1:
                        BusSWnum[ii + 1] = ApunN[j]
                    else:
                        BusSWnum[ii + 1] = -100
            objeto.dssLines.Next

        NamePobSw = ["" for x in range(objeto.dssSwitch.Count)]
        for i in range(len(NameLinSw)):
            objeto.dssSwitch.First
            for j in range(len(NameLinSw)):
                Ncompleto = objeto.dssSwitch.SwitchedObj
                TipoEl, NombSw = Ncompleto.split('.')
                if NameLinSw[i] == NombSw:
                    NamePobSw[i] = objeto.dssSwitch.Name
                objeto.dssSwitch.Next

        if TipoDsimulacion == "ConControlDReg" or TipoDsimulacion == "ConRegSinReconf" or TipoDsimulacion == "TotalOpt":
            NameRegs = objeto.dssRegControls.AllNames
            Nreg = len(NameRegs)
            PosicionesReg = Nreg*6
            Trcontroled = np.zeros((len(NameRegs)))
            Trcontroled = Trcontroled.tolist()
            objeto.dssRegControls.First
            for i in range(len(NameRegs)):
                objeto.dssCircuit.setActiveElement("regcontrol." + NameRegs[i])
                Trcontroled[i] = objeto.dssRegControls.Transformer
                objeto.dssCktElement.Properties("enabled").Val = False
                objeto.dssRegControls.Next
        else:
            NameRegs = objeto.dssRegControls.AllNames
            Trcontroled = np.zeros((len(NameRegs)))

        if TipoDsimulacion == "BancoCap" or TipoDsimulacion == "TotalOpt" or TipoDsimulacion == "TotalSinReg" or TipoDsimulacion == "BCapLocked":
            NameCaps = objeto.dssCapacitors.AllNames
            CapN = objeto.dssCapacitors.Count

        if TipoDsimulacion == "BancoCap" or TipoDsimulacion == "ConRegSinReconf" or TipoDsimulacion == "SoloPV" or TipoDsimulacion == "BCapLocked" or TipoDsimulacion == "PVLocked":
            NombreLlaves = objeto.dssSwitch.AllNames
            LlaveamientoOriginal = np.array([[1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0,	0, 0, 0, 1, 1]])

            for j in range(len(NombreLlaves)):
                if LlaveamientoOriginal[0, j] == 0:
                    nombre = NombreLlaves[j]
                    objeto.dssText.Command = "edit swtcontrol." + nombre + " state=open"
                else:
                    nombre = NombreLlaves[j]
                    objeto.dssText.Command = "edit swtcontrol." + nombre + " state=closed"


        ALLTransf=objeto.dssTransformers.AllNames
        NTransf=size(ALLTransf)
        BusT = np.zeros((NTransf*2))
        BusT = BusT.tolist()
        BusTnum = np.zeros((NTransf * 2))
        ntraux = 0
        ctaux = 0
        Repeated = 0
        if ALLTransf[0] != 'NONE':
            objeto.dssTransformers.First
            for i in range(NTransf):
                barra1, barra2 = objeto.buses()
                if barra1.find(".") != -1:
                    barra1, mins = barra1.split('.')
                if barra2.find(".") != -1:
                    barra2, mins = barra2.split('.')
                for x in range(ntraux*2):
                    if BusT[x] == barra1:
                        for xx in range(ntraux*2):
                            if BusT[xx] == barra2:
                                Repeated = 1
                if Repeated == 0:
                    BusT[ctaux] = barra1
                    BusT[ctaux+1] = barra2
                    for j in range(NB):
                        if BusT[ctaux] == Busnames[j]:
                            BusTnum[ctaux] = ApunN[j]
                        if BusT[ctaux + 1] == Busnames[j]:
                            BusTnum[ctaux + 1] = ApunN[j]
                    ctaux = ctaux + 2
                ntraux = ntraux + 1
                Repeated = 0

                objeto.dssTransformers.Next

        exists = 0 in BusT
        if exists == True:
            zerocorte = BusT.index(0)
            BusT = BusT[:zerocorte]
            NTransf = int(zerocorte/2)

        NLL=objeto.dssSwitch.Count
        BusWeight1=np.zeros((3, NLin-NLL))
        BusWeight2=np.zeros((3, NLL))
        LineLengths1 = np.zeros((3, NLin-NLL))
        LineLengths2 = np.zeros((3, NLL))
        Vaux = objeto.dssCircuit.AllBusVolts


        j = 0
        jj = 0
        for i in range(NLin):
            ii = i * 2
            if BusSWnum[ii]==-100 and BusSWnum[ii+1]==-100:
                BusWeight1[0, jj] = BusLnum[ii]
                BusWeight1[1, jj] = BusLnum[ii + 1]
                BusWeight1[2, jj] = 0.01
                LineLengths1[0, jj] = BusLnum[ii]
                LineLengths1[1, jj] = BusLnum[ii + 1]
                LineLengths1[2, jj] = LineLengths[i]

                jj = jj + 1
            else:
                BusWeight2[0, j] = BusLnum[ii]
                BusWeight2[1, j] = BusLnum[ii + 1]
                BusWeight2[2, j] = 1
                LineLengths2[0, j] = BusLnum[ii]
                LineLengths2[1, j] = BusLnum[ii + 1]
                LineLengths2[2, j] = LineLengths[i]
                j = j + 1

        serie = int((ii + 2) / 2)
        BusWeight = np.concatenate((BusWeight2, BusWeight1), axis=1)
        BTaux = np.zeros((3, NTransf))
        BTaux2 = np.concatenate((BusWeight, BTaux), axis=1)
        LineLengths = np.concatenate((LineLengths2, LineLengths1), axis=1)
        LineLengths = np.concatenate((LineLengths, BTaux), axis=1)

        if ALLTransf[0] != 'NONE':
            ii = int((ii + 2) / 2)
            for i in range(NTransf):
                j = i * 2
                BTaux2[0, ii] = BusTnum[j]
                BTaux2[1, ii] = BusTnum[j + 1]
                BTaux2[2, ii] = 0.01
                LineLengths[0, ii] = BusTnum[j]
                LineLengths[1, ii] = BusTnum[j + 1]
                LineLengths[2, ii] = 0.00001
                ii = ii+1
            serie = ii
        BusWeight=BTaux2

        from BuscaBarras import BarrasconPV
        NBC, Load_fases, NbLoad = BarrasconPV(objeto)

        Barras3F_PV =  [''] * len(Busnames)

        j = 0
        for i in range(len(Busnames)):
            objeto.dssCircuit.SetActiveBus(Busnames[i])
            VoltajeBus = objeto.dssBus.kVBase
            NroFasesBarra = len(objeto.dssBus.Nodes)
            if NroFasesBarra > 2 and VoltajeBus > 2 and Busnames[i] != '150' and Busnames[i] != '150r' and Busnames[i] != '149' and Busnames[i] != '160r' and Busnames[i] != '61s':
                Barras3F_PV[j] = Busnames[i]
                j = j + 1

        while '' in Barras3F_PV:
            Barras3F_PV.remove('')

        objeto.dssText.Command = "set loadmult=0.4"

        CantidadInicialPvs = 17
        from Aleatorio_PV import PosicionesDePVs
        BusDomAleatorio = PosicionesDePVs(NBC, Semilla, CantidadInicialPvs)

        if SistemaConPv == "SI":
            TOTALbname = objeto.dssCircuit.AllBusNames
            bnameSelected = BusDomAleatorio
            CtdPV = len(bnameSelected)
            NBCaux = NBC[0, :]
            NBCaux = [int(x) for x in NBCaux]
            NBCaux = [str(x) for x in NBCaux]

            for i in range(CtdPV):
                bname=bnameSelected[i]
                PosicionBusPV = np.argwhere(np.array(NBCaux) == bname)
                NBCind = NBC[:, PosicionBusPV]
                Load_fasesInd = Load_fases[:, PosicionBusPV]
                from PV_Rand import PVparameters
                VPV = PVparameters(objeto, bname, NBCind, Load_fasesInd)
        else:
            CtdPV = 0

        objeto.dssText.Command = "edit transformer.reg1a XHL=0.000001 %LoadLoss=0.000001 "

        if TipoDsimulacion == "ConControlDReg":
            bits = NLL + PosicionesReg
        elif TipoDsimulacion == "SinControlDReg" or TipoDsimulacion == "ReconfLocked":
            bits = NLL
        elif TipoDsimulacion == "ConRegSinReconf":
            bits = PosicionesReg
        elif TipoDsimulacion == "BancoCap" or TipoDsimulacion == "BCapLocked":
            bits = CapN
        elif TipoDsimulacion == "SoloPV" or TipoDsimulacion == "PVLocked":
            bits = 4 * 2
        elif TipoDsimulacion == "TotalOpt":
            bits = NLL + PosicionesReg + CapN + 4 * 2
        elif TipoDsimulacion == "TotalSinReg":
            bits = NLL +  CapN + 4 * 2

        BarrasConPVs = np.zeros((individuos * 2 * 2, NBC.shape[1]))

        import numpy as np

        if TipoDsimulacion == "ConControlDReg":
            poblacion = np.zeros((individuos, NLL + PosicionesReg))
        elif TipoDsimulacion == "SinControlDReg" or TipoDsimulacion == "ReconfLocked":
            poblacion = np.zeros((individuos, NLL))
        elif TipoDsimulacion == "ConRegSinReconf":
            poblacion = np.zeros((individuos, PosicionesReg))
        elif TipoDsimulacion == "BancoCap" or TipoDsimulacion == "BCapLocked":
            poblacion = np.zeros((individuos, CapN))
        elif TipoDsimulacion == "SoloPV" or TipoDsimulacion == "PVLocked":
            poblacion = np.zeros((individuos, 4 * 2))
        elif TipoDsimulacion == "TotalOpt":
            poblacion = np.zeros((individuos, NLL + PosicionesReg + CapN + 4 * 2))
        elif TipoDsimulacion == "TotalSinReg":
            poblacion = np.zeros((individuos, NLL + CapN + 4 * 2))

        PoblacionSinOrden = np.zeros((individuos * 2, poblacion.shape[1]))

        if TipoDsimulacion == "ConControlDReg":
            for i in range(individuos):
                poblacion[i, :] = np.random.randint(2, size=NLL+PosicionesReg)
        elif TipoDsimulacion == "SinControlDReg" or TipoDsimulacion == "ReconfLocked":
            for i in range(individuos):
                poblacion[i, :] = np.random.randint(2, size=NLL)
        elif TipoDsimulacion == "ConRegSinReconf":
            for i in range(individuos):
                poblacion[i, :] = np.random.randint(2, size=PosicionesReg)
        elif TipoDsimulacion == "BancoCap" or TipoDsimulacion == "BCapLocked":
            for i in range(individuos):
                poblacion[i, :] = np.random.randint(2, size=CapN)
        elif TipoDsimulacion == "SoloPV" or TipoDsimulacion == "PVLocked":
            for i in range(individuos):
                poblacion[i, :] = np.random.randint(2, size=4 * 2)
        elif TipoDsimulacion == "TotalOpt":
            for i in range(individuos):
                poblacion[i, :] = np.random.randint(2, size=NLL + PosicionesReg + CapN + 4 * 2)
        elif TipoDsimulacion == "TotalSinReg":
            for i in range(individuos):
                poblacion[i, :] = np.random.randint(2, size=NLL + CapN + 4 * 2)

        poblacion = poblacion.astype(int)
        LOSS = np.zeros(individuos*2)
        Vaux = np.zeros(NB)
        VB = np.zeros((3, NB),dtype=np.complex_)
        HCindiv = np.zeros(individuos)
        HCindivMenor = np.zeros(individuos)
        LOSSmenor = np.zeros(individuos)
        VUF = np.zeros(NB)

        for z in range(iteraciones):
            if TipoDsimulacion == "ConControlDReg":
                pobaux = poblacion[: , NLL:NLL+PosicionesReg]
                poblacion = poblacion[: , 0:NLL]
            elif TipoDsimulacion == "TotalOpt":
                pobaux = poblacion[: , NLL:NLL + PosicionesReg + CapN + 4 * 2]
                poblacion = poblacion[: , 0:NLL]
            elif TipoDsimulacion == "TotalSinReg":
                pobaux = poblacion[: , NLL:NLL + CapN + 4 * 2]
                poblacion = poblacion[: , 0:NLL]
            if TipoDsimulacion == "ConControlDReg" or TipoDsimulacion == "SinControlDReg" or TipoDsimulacion == "TotalOpt" or TipoDsimulacion == "TotalSinReg" or TipoDsimulacion == "ReconfLocked":
                from radial import rad
                poblacion=rad(poblacion, BusWeight, NB, NLL, individuos, serie)
            if TipoDsimulacion == "ConControlDReg" or TipoDsimulacion == "TotalOpt" or TipoDsimulacion == "TotalSinReg":
                poblacion = np.concatenate((poblacion, pobaux), axis=1)

            R = poblacion
            poblfinal = poblacion

            if z == 0:

                def PowerFlow(individuos, NLL, poblacion, NB, NameRegs, Trcontroled, BusDomAleatorio, CantidadInicialPvs, NBC, Semilla, NBCaux, Barras3F_PV, BarrasConPVs, PoblacionSinOrden):

                    LOSS = np.zeros(individuos)
                    HCindiv = np.zeros(individuos)
                    LOSSmenor = np.zeros(individuos)
                    HCindivMenor = np.zeros(individuos)
                    CantidadInicialPvs_Auxiliar = CantidadInicialPvs
                    BusDomAleatorio_Auxiliar = BusDomAleatorio
                    for i in range(individuos):
                        PvCero = objeto.dssPV.AllNames
                        for j in range(len(objeto.dssPV.AllNames)):
                            objeto.dssText.Command = "edit transformer.PV_" + PvCero[j] + " kVAs=(" + str(0.0001) + ", " + str(0.0001) + ")"
                            objeto.dssText.Command = "edit PVSystem.PV_" + PvCero[j] + " kVA=" + str(0.0001) + " Pmpp=" + str(0.0001)
                        CantidadInicialPvs = CantidadInicialPvs_Auxiliar
                        CountNewPV = CantidadInicialPvs
                        BusDomAleatorio = BusDomAleatorio_Auxiliar
                        InfVol = False
                        Infcorr = False
                        InfVUFfinal = False
                        InfVDeviation = False
                        incremento = 0
                        bnameSelected = BusDomAleatorio
                        VectorIncremento = np.zeros((len(bnameSelected)))
                        bnameMarcado = np.zeros((len(bnameSelected)))
                        HC = 0
                        MultPV_incremento = 10
                        Incremento_Planta = 1000
                        BarrasConPVs[i * 2 + 1, :] = 0
                        if TipoDsimulacion == "SinControlDReg" or TipoDsimulacion == "BancoCap" or TipoDsimulacion == "SoloPV" or TipoDsimulacion == "TotalSinReg":
                            NameRegs = objeto.dssRegControls.AllNames
                            Trcontroled = np.zeros((len(NameRegs)))
                            Trcontroled = Trcontroled.tolist()
                            objeto.dssRegControls.First
                            for j in range(len(NameRegs)):
                                objeto.dssText.Command = "Reset EventLog"
                                Trcontroled[j] = objeto.dssRegControls.Transformer
                                objeto.dssCircuit.Transformers.Name = Trcontroled[j]
                                objeto.dssCircuit.Transformers.wdg = 2
                                objeto.dssText.Command = "edit regcontrol." + NameRegs[j] + " Reset=Yes"
                                objeto.dssCtrlQueue.ClearActions()
                                objeto.dssCtrlQueue.ClearQueue()
                                objeto.dssCtrlQueue.Delete(0)
                                objeto.dssCtrlQueue.DoAllQueue()
                                objeto.dssRegControls.Next
                        PrimerVdeviation = True
                        Barras3F_PV_AUX = Barras3F_PV
                        Cantidad_Plantas = 0
                        Ya_Elegido_Planta = np.zeros((len(bnameSelected)))
                        Vector_Plantas = '0'
                        BarraPlanta_Aleatoria = np.ones(1)
                        maxPowerbname = np.zeros((len(bnameSelected)))

                        while InfVol == False and Infcorr == False and InfVUFfinal == False and InfVDeviation == False:
                            MultPV = MultPV_incremento * incremento
                            VectorMultPV = MultPV_incremento * VectorIncremento
                            PVporBarraAux = np.zeros((len(bnameSelected)))
                            Cerar_Elegido_Vector = True
                            for j in range(len(bnameSelected)):
                                Vec1 = NBC[0, :]
                                ValBuscar = bnameSelected[j]
                                posicionElemento = posicionRep(Vec1, ValBuscar)
                                if maxPowerbname[j] == 0:
                                    maxPowerbname[j] = NBC[3, posicionElemento]
                                PVporBarraAux[j] = MultPV
                                if maxPowerbname[j] + 20 < VectorMultPV[j] and bnameMarcado[j] == 0:
                                    bnameMarcado[j] = 1
                                    if len(bnameMarcado) < len(NBC[0, :]):
                                        CantidadInicialPvs += 1
                                        from Aleatorio_PV import PosicionesDePVs
                                        BusDomAleatorio = PosicionesDePVs(NBC, Semilla, CantidadInicialPvs)
                                        bnameSelected = BusDomAleatorio
                                        bnameMarcado = np.append(bnameMarcado, 0)
                                        VectorIncremento = np.append(VectorIncremento, 0)
                                        VectorMultPV = np.append(VectorMultPV, 0.0001)
                                        Ya_Elegido_Planta = np.append(Ya_Elegido_Planta, 0)
                                        maxPowerbname = np.append(maxPowerbname, 0)
                                Prueba_Entero = CantidadInicialPvs/20
                                if Prueba_Entero.is_integer() == True:
                                    Vector_bnameActual = bnameSelected[0:j+1]
                                    Se_agrego_Planta = False
                                    SalePlanta = False
                                    random.seed(Semilla)
                                    if Cerar_Elegido_Vector == True:
                                        Elegido_Vector_bnameActual = np.zeros((len(Vector_bnameActual)))
                                    else:
                                        for jjj in range(len(Vector_bnameActual) - len(Elegido_Vector_bnameActual)):
                                            Elegido_Vector_bnameActual = np.append(Elegido_Vector_bnameActual, 0)
                                    Cerar_Elegido_Vector = False
                                    while SalePlanta == False:
                                        Potencial_barra = random.sample(Vector_bnameActual, 1)
                                        for jjj in range(len(Vector_bnameActual)):
                                            if Vector_bnameActual[jjj] == Potencial_barra[0]:
                                                Elegido_Vector_bnameActual[jjj] = 1
                                                Posicion_Elegido = jjj
                                        EncuentraBarra = False
                                        for jjj in range(len(BarraPlanta_Aleatoria)):
                                            if Potencial_barra[0] == BarraPlanta_Aleatoria[jjj]:
                                                EncuentraBarra = True
                                        if EncuentraBarra == True:
                                            SalePlanta = False
                                        else:
                                            SalePlanta = True
                                            if BarraPlanta_Aleatoria[0] == 1:
                                                BarraPlanta_Aleatoria = Potencial_barra
                                                maxPowerbname[Posicion_Elegido] = maxPowerbname[Posicion_Elegido] + Incremento_Planta
                                                bnameMarcado[Posicion_Elegido] = 0
                                            else:
                                                BarraPlanta_Aleatoria = np.append(BarraPlanta_Aleatoria, Potencial_barra)
                                                maxPowerbname[Posicion_Elegido] = maxPowerbname[Posicion_Elegido] + Incremento_Planta
                                                bnameMarcado[Posicion_Elegido] = 0

                                        if np.sum(Elegido_Vector_bnameActual) == len(Elegido_Vector_bnameActual):
                                            SalePlanta = True
                                    for jjj in range(len(Vector_bnameActual)):
                                        if Ya_Elegido_Planta[jjj] == 0 and Se_agrego_Planta == False:
                                            if len(Vector_Plantas) == 1:
                                                Vector_Plantas = BarraPlanta_Aleatoria
                                            else:
                                                Vector_Plantas = np.append(Vector_Plantas, BarraPlanta_Aleatoria)
                                            Se_agrego_Planta = True
                                            Ya_Elegido_Planta[jjj] = 1
                            CtdPV = len(bnameSelected)
                            if TipoDsimulacion == "ConControlDReg" or TipoDsimulacion == "SinControlDReg" or TipoDsimulacion == "TotalOpt"  or TipoDsimulacion == "TotalSinReg" or TipoDsimulacion == "ReconfLocked":
                                for j in range(NLL):
                                    if poblacion[i, j] == 0:
                                        nombre = NamePobSw[j]
                                        objeto.dssText.Command = "edit swtcontrol." + nombre + " state=open"
                                        objeto.dssSwitch.Name = nombre
                                    else:
                                        nombre = NamePobSw[j]
                                        objeto.dssText.Command = "edit swtcontrol." + nombre + " state=closed"
                                        objeto.dssSwitch.Name = nombre
                            if TipoDsimulacion == "ConControlDReg" or TipoDsimulacion == "ConRegSinReconf" or TipoDsimulacion == "TotalOpt":
                                if TipoDsimulacion == "ConControlDReg" or TipoDsimulacion == "TotalOpt":
                                    RegBinary = poblacion[:, NLL:NLL+PosicionesReg]
                                    for j in range(len(NameRegs)):
                                        RegBinarySeparado = np.array(RegBinary[i, j * 6:j * 6 + 6])
                                        Unificado, Decimal = VecToNum(RegBinarySeparado)
                                        poblacion[i, NLL + j * 6:NLL + j * 6 + 6] = Unificado
                                        objeto.dssTransformers.Name = Trcontroled[j]
                                        objeto.dssTransformers.wdg = 2
                                        newTap = Decimal
                                        objeto.dssTransformers.Tap = 1 + newTap * 0.00625
                                if TipoDsimulacion == "ConRegSinReconf":
                                    RegBinary = poblacion
                                    for j in range(len(NameRegs)):
                                        RegBinarySeparado = np.array(RegBinary[i, j * 6:j * 6 + 6])
                                        Unificado, Decimal = VecToNum(RegBinarySeparado)
                                        poblacion[i, j * 6:j * 6 + 6] = Unificado
                                        objeto.dssTransformers.Name = Trcontroled[j]
                                        objeto.dssTransformers.wdg = 2
                                        newTap = Decimal
                                        objeto.dssTransformers.Tap = 1 + newTap * 0.00625
                            if TipoDsimulacion == "BancoCap" or TipoDsimulacion == "BCapLocked":
                                for j in range(len(NameCaps)):
                                    if poblacion[i, j] == 0:
                                        nombre = NameCaps[j]
                                        objeto.dssCapacitors.Name = nombre
                                        objeto.dssCapacitors.States = (0,)
                                    else:
                                        nombre = NameCaps[j]
                                        objeto.dssCapacitors.Name = nombre
                                        objeto.dssCapacitors.States = (1,)
                            if TipoDsimulacion == "TotalOpt":
                                for j in range(NLL+PosicionesReg, NLL + PosicionesReg + CapN):
                                    if poblacion[i, j] == 0:
                                        nombre = NameCaps[j-(NLL+PosicionesReg)]
                                        objeto.dssCapacitors.Name = nombre
                                        objeto.dssCapacitors.States = (0,)
                                    else:
                                        nombre = NameCaps[j-(NLL+PosicionesReg)]
                                        objeto.dssCapacitors.Name = nombre
                                        objeto.dssCapacitors.States = (1,)
                            if TipoDsimulacion == "TotalSinReg":
                                for j in range(NLL, NLL + CapN):
                                    if poblacion[i, j] == 0:
                                        nombre = NameCaps[j-(NLL)]
                                        objeto.dssCapacitors.Name = nombre
                                        objeto.dssCapacitors.States = (0,)
                                    else:
                                        nombre = NameCaps[j-(NLL)]
                                        objeto.dssCapacitors.Name = nombre
                                        objeto.dssCapacitors.States = (1,)
                            if TipoDsimulacion == "SoloPV" or TipoDsimulacion == "TotalSinReg" or TipoDsimulacion == "PVLocked" or TipoDsimulacion == "TotalOpt":
                                Llaveamiento = np.array([1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0,	0, 0, 0, 1, 1])
                                from Dijkstra import DJ
                                distArray = DJ(Llaveamiento, BusWeight, NB, NLL, individuos, serie, LineLengths, objeto)
                                VecDistancias = np.zeros((len(bnameSelected)))
                                for j in range(len(bnameSelected)):
                                    PosicionPV = np.argwhere(Busnames == bnameSelected[j])
                                    PosicionPVaux = PosicionPV[0,0].astype(int)
                                    if distArray[PosicionPVaux] < 1.5:
                                        VecDistancias[j] = 1
                                    elif distArray[PosicionPVaux] >= 1.5 and distArray[PosicionPVaux] < 3:
                                        VecDistancias[j] = 2
                                    elif distArray[PosicionPVaux] >= 3 and distArray[PosicionPVaux] < 4.5:
                                        VecDistancias[j] = 3
                                    if distArray[PosicionPVaux] >= 4.5:
                                        VecDistancias[j] = 4
                            if TipoDsimulacion == "SoloPV" or TipoDsimulacion == "PVLocked":
                                jInicial = 0
                                jFinal = 4 * 2
                                jSalto = 2
                            if TipoDsimulacion == "TotalOpt":
                                jInicial = NLL + PosicionesReg + CapN
                                jFinal = NLL + PosicionesReg + CapN + 4 * 2
                                jSalto = 2
                            if TipoDsimulacion == "TotalSinReg":
                                jInicial = NLL + CapN
                                jFinal = NLL + CapN + 4 * 2
                                jSalto = 2
                            if TipoDsimulacion == "SoloPV" or TipoDsimulacion == "PVLocked" or TipoDsimulacion == "TotalOpt" or TipoDsimulacion == "TotalSinReg":
                                for j in range(jInicial, jFinal, jSalto):
                                    if j == 0:
                                        for ii in range(len(bnameSelected)):
                                            nombre = bnameSelected[ii]
                                            if poblacion[i, j] == 0 and poblacion[i, j+1] == 0 and VecDistancias[ii] == 1:
                                                objeto.dssText.Command = "edit InvControl.VoltVar_" + nombre + " vvc_curve1=NoReactivo"
                                            elif poblacion[i, j] == 0 and poblacion[i, j+1] == 1 and VecDistancias[ii] == 1:
                                                objeto.dssText.Command = "edit InvControl.VoltVar_" + nombre + " vvc_curve1=IEEE1547regA"
                                            elif poblacion[i, j] == 1 and poblacion[i, j+1] == 0 and VecDistancias[ii] == 1:
                                                objeto.dssText.Command = "edit InvControl.VoltVar_" + nombre + " vvc_curve1=IEEE1547regB"
                                            elif poblacion[i, j] == 1 and poblacion[i, j+1] == 1 and VecDistancias[ii] == 1:
                                                objeto.dssText.Command = "edit InvControl.VoltVar_" + nombre + " vvc_curve1=MayorReactivo"
                                    if j == 2:
                                        for ii in range(len(bnameSelected)):
                                            nombre = bnameSelected[ii]
                                            if poblacion[i, j] == 0 and poblacion[i, j+1] == 0 and VecDistancias[ii] == 2:
                                                objeto.dssText.Command = "edit InvControl.VoltVar_" + nombre + " vvc_curve1=NoReactivo"
                                            elif poblacion[i, j] == 0 and poblacion[i, j+1] == 1 and VecDistancias[ii] == 2:
                                                objeto.dssText.Command = "edit InvControl.VoltVar_" + nombre + " vvc_curve1=IEEE1547regA"
                                            elif poblacion[i, j] == 1 and poblacion[i, j+1] == 0 and VecDistancias[ii] == 2:
                                                objeto.dssText.Command = "edit InvControl.VoltVar_" + nombre + " vvc_curve1=IEEE1547regB"
                                            elif poblacion[i, j] == 1 and poblacion[i, j+1] == 1 and VecDistancias[ii] == 2:
                                                objeto.dssText.Command = "edit InvControl.VoltVar_" + nombre + " vvc_curve1=MayorReactivo"
                                    if j == 4:
                                        for ii in range(len(bnameSelected)):
                                            nombre = bnameSelected[ii]
                                            if poblacion[i, j] == 0 and poblacion[i, j+1] == 0 and VecDistancias[ii] == 3:
                                                objeto.dssText.Command = "edit InvControl.VoltVar_" + nombre + " vvc_curve1=NoReactivo"
                                            elif poblacion[i, j] == 0 and poblacion[i, j+1] == 1 and VecDistancias[ii] == 3:
                                                objeto.dssText.Command = "edit InvControl.VoltVar_" + nombre + " vvc_curve1=IEEE1547regA"
                                            elif poblacion[i, j] == 1 and poblacion[i, j+1] == 0 and VecDistancias[ii] == 3:
                                                objeto.dssText.Command = "edit InvControl.VoltVar_" + nombre + " vvc_curve1=IEEE1547regB"
                                            elif poblacion[i, j] == 1 and poblacion[i, j+1] == 1 and VecDistancias[ii] == 3:
                                                objeto.dssText.Command = "edit InvControl.VoltVar_" + nombre + " vvc_curve1=MayorReactivo"
                                    if j == 6:
                                        for ii in range(len(bnameSelected)):
                                            nombre = bnameSelected[ii]
                                            if poblacion[i, j] == 0 and poblacion[i, j+1] == 0 and VecDistancias[ii] == 4:
                                                objeto.dssText.Command = "edit InvControl.VoltVar_" + nombre + " vvc_curve1=NoReactivo"
                                            elif poblacion[i, j] == 0 and poblacion[i, j+1] == 1 and VecDistancias[ii] == 4:
                                                objeto.dssText.Command = "edit InvControl.VoltVar_" + nombre + " vvc_curve1=IEEE1547regA"
                                            elif poblacion[i, j] == 1 and poblacion[i, j+1] == 0 and VecDistancias[ii] == 4:
                                                objeto.dssText.Command = "edit InvControl.VoltVar_" + nombre + " vvc_curve1=IEEE1547regB"
                                            elif poblacion[i, j] == 1 and poblacion[i, j+1] == 1 and VecDistancias[ii] == 4:
                                                objeto.dssText.Command = "edit InvControl.VoltVar_" + nombre + " vvc_curve1=MayorReactivo"
                            for j in range(CtdPV):
                                if j >= CountNewPV-1:
                                    if CountNewPV > len(objeto.dssPV.AllNames):
                                        bname = bnameSelected[j]
                                        PosicionBusPV = np.argwhere(np.array(NBCaux) == bname)
                                        NBCind = NBC[:, PosicionBusPV]
                                        Load_fasesInd = Load_fases[:, PosicionBusPV]
                                        from PV_Rand import PVparameters
                                        PVparameters(objeto, bname, NBCind, Load_fasesInd)
                                    CountNewPV += 1
                            for j in range(CtdPV):
                                if incremento == 0:
                                    objeto.dssText.Command = "edit transformer.PV_" + bnameSelected[j] + " kVAs=(" + str(0.00001) + ", " + str(0.00001) + ")"
                                    objeto.dssText.Command = "edit PVSystem.PV_" + bnameSelected[j] + " kVA=" + str(0.00001) + " Pmpp=" + str(0.00001)
                                else:
                                    objeto.dssText.Command = "edit transformer.PV_" + bnameSelected[j] + " kVAs=(" + str(VectorMultPV[j]) + ", " + str(VectorMultPV[j]) + ")"
                                    objeto.dssText.Command = "edit PVSystem.PV_" + bnameSelected[j] + " kVA=" + str(VectorMultPV[j]) + " Pmpp=" + str(VectorMultPV[j])
                            if (TipoDsimulacion == "ReconfLocked" or TipoDsimulacion == "BCapLocked" or TipoDsimulacion == "PVLocked") and HC > 0:
                                for j in range(len(NameRegs)):
                                    objeto.dssTransformers.Name = Trcontroled[j]
                                    objeto.dssTransformers.wdg = 2
                                    objeto.dssTransformers.Tap = TapFijo[j]

                            if (TipoDsimulacion == "ReconfLocked" or TipoDsimulacion == "BCapLocked" or TipoDsimulacion == "PVLocked") and incremento == 0:
                                NameRegs = objeto.dssRegControls.AllNames
                                Trcontroled = np.zeros((len(NameRegs)))
                                Trcontroled = Trcontroled.tolist()
                                objeto.dssRegControls.First
                                for j in range(len(NameRegs)):
                                    objeto.dssCircuit.setActiveElement("regcontrol." + NameRegs[j])
                                    objeto.dssCktElement.Properties("enabled").Val = True
                                    objeto.dssText.Command = "Reset EventLog"
                                    Trcontroled[j] = objeto.dssRegControls.Transformer
                                    objeto.dssCircuit.Transformers.Name = Trcontroled[j]
                                    objeto.dssCircuit.Transformers.wdg = 2
                                    objeto.dssText.Command = "edit regcontrol." + NameRegs[j] + " Reset=Yes"
                                    objeto.dssCtrlQueue.ClearActions()
                                    objeto.dssCtrlQueue.ClearQueue()
                                    objeto.dssCtrlQueue.Delete(0)
                                    objeto.dssCtrlQueue.DoAllQueue()
                                    objeto.dssRegControls.Next
                            objeto.dssSolution.Solve()
                            PoblacionSinOrden[i, :] = poblacion[i, :]
                            if (TipoDsimulacion == "ReconfLocked" or TipoDsimulacion == "BCapLocked" or TipoDsimulacion == "PVLocked") and incremento == 0:
                                TapFijo = np.zeros(len(NameRegs))
                                Trcontroled = np.zeros((len(NameRegs)))
                                Trcontroled = Trcontroled.tolist()
                                objeto.dssRegControls.First
                                for j in range(len(NameRegs)):
                                    objeto.dssCircuit.setActiveElement("regcontrol." + NameRegs[j])
                                    Trcontroled[j] = objeto.dssRegControls.Transformer
                                    objeto.dssCktElement.Properties("enabled").Val = False
                                    objeto.dssTransformers.Name = Trcontroled[j]
                                    objeto.dssTransformers.wdg = 2
                                    TapFijo[j] = objeto.dssTransformers.Tap
                                    objeto.dssRegControls.Next
                            TODASPERDIDAS = objeto.dssCircuit.AllElementLosses
                            TODASPERDIDASaux = TODASPERDIDAS[0:len(objeto.dssCircuit.AllElementLosses):2]
                            Voltages = objeto.dssCircuit.AllBusVmagpu
                            v_max = max(Voltages)
                            v_min = min(Voltages)
                            VMINposicion = np.argwhere(np.array(Voltages) == v_min)
                            if v_max > 1.1 or v_min < 0.90:
                                InfVol = True

                            CORRIENTELINEAS = np.zeros(objeto.dssLines.count)
                            objeto.dssLines.First
                            for j in range(objeto.dssLines.count):
                                objeto.dssCircuit.SetActiveElement("line." + objeto.dssLines.Name)
                                if objeto.dssLines.LineCode == "1" or objeto.dssLines.LineCode == "2" or objeto.dssLines.LineCode == "3" or objeto.dssLines.LineCode == "4" or objeto.dssLines.LineCode == "5" or objeto.dssLines.LineCode == "6" or objeto.dssLines.LineCode == "7" or objeto.dssLines.LineCode == "8":
                                    objeto.dssText.Command = "edit line." + objeto.dssLines.Name + " normamps=529"
                                elif objeto.dssLines.LineCode == "9" or objeto.dssLines.LineCode == "10" or objeto.dssLines.LineCode == "11":
                                    objeto.dssText.Command = "edit line." + objeto.dssLines.Name + " normamps=242"
                                else:
                                    objeto.dssText.Command = "edit line." + objeto.dssLines.Name + " normamps=529"
                                Corriente = objeto.dssCktElement.CurrentsMagAng
                                CorrienteNominal = objeto.dssLines.NormAmps
                                CORRIENTELINEAS[j] = max(Corriente[0:12:2])
                                if max(Corriente[0:12:2]) > CorrienteNominal:
                                    Infcorr = True
                                objeto.dssLines.Next

                            VUFrestr = np.zeros((NB))
                            for j in range(NB):
                                objeto.dssCircuit.SetActiveBus(Busnames[j])
                                if objeto.dssBus.SeqVoltages[2] != objeto.dssBus.SeqVoltages[1] and np.isnan(objeto.dssBus.SeqVoltages[1]) == False and np.isnan(objeto.dssBus.SeqVoltages[2]) == False:
                                    VUFrestr[j] = objeto.dssBus.SeqVoltages[2] / objeto.dssBus.SeqVoltages[1] * 100
                                else:
                                    VUFrestr[j] = 0
                            VUFfinal = max(VUFrestr)

                            if VUFfinal > 2:
                                InfVUFfinal = True
                            if PrimerVdeviation == True:
                                Array_Deviation = np.zeros(len(Voltages))
                                for j in range(len(Array_Deviation)):
                                    Array_Deviation[j] = Voltages[j]
                            for j in range(len(Array_Deviation)):
                                if abs((Voltages[j] - Array_Deviation[j]) / Voltages[j] * 100) > 0.055:
                                    InfVDeviation = True
                            PrimerVdeviation = False
                            aux = objeto.dssCircuit.Losses
                            LOSS[i] = aux[0]
                            if InfVol == False and Infcorr == False and InfVUFfinal == False:
                                LOSS_aux = LOSS[i]
                                HC = sum(VectorMultPV)
                                HC = math.trunc(HC)
                                for j in range(len(bnameSelected)):
                                    BarrasConPVs[i*2, j] = bnameSelected[j]
                                    BarrasConPVs[i*2+1, j] = math.trunc(VectorMultPV[j])
                                if HC == 0:
                                    LOSSmenor[i] = LOSS_aux
                                    HCindivMenor[i] = HC
                                if LOSS_aux < LOSSmenor[i]:
                                    LOSSmenor[i] = LOSS_aux
                                    HCindivMenor[i] = HC
                            else:
                                if HC == 0 and InfVol == True:
                                    LOSS_aux = LOSS[i]*10
                                    LOSSmenor[i] = LOSS[i]
                                    HCindivMenor[i] = HC
                                if HC == 0 and Infcorr == True:
                                    LOSS_aux = LOSS[i]*10
                                    LOSSmenor[i] = LOSS[i]
                                    HCindivMenor[i] = HC
                                if HC == 0 and InfVUFfinal == True:
                                    LOSS_aux = LOSS[i]*10
                                    LOSSmenor[i] = LOSS[i]
                                    HCindivMenor[i] = HC
                                LOSS[i] = LOSS_aux
                            HCindiv[i] = HC
                            for j in range(i-1):
                                RepetidoAux = True
                                for jj in range(poblacion.shape[1]):
                                    if (poblacion[i, jj] != poblacion[j, jj]) and RepetidoAux == True:
                                        RepetidoAux = False
                                if RepetidoAux == True:
                                    HCindiv[i] = -111 * random.randint(1, 20)
                                    LOSS[i] = LOSS[i] * 20 * random.randint(1, 20)
                            incremento += 1
                            for j in range(len(bnameSelected)):
                                if bnameMarcado[j] == 1:
                                    VectorIncremento[j] = VectorIncremento[j]
                                else:
                                    VectorIncremento[j] = 1 + VectorIncremento[j]
                            if CtdPV ==0:
                                InfVol = True
                                Infcorr = True
                                InfVUFfinal = True
                            if HCindiv[i] > 50000:
                                exit()

                    return HCindiv, LOSS, HCindivMenor, LOSSmenor, BarrasConPVs, PoblacionSinOrden
                HCindiv, LOSS, HCindivMenor, LOSSmenor, BarrasConPVs, PoblacionSinOrden = PowerFlow(individuos, NLL, poblacion, NB, NameRegs, Trcontroled, BusDomAleatorio, CantidadInicialPvs, NBC, Semilla, NBCaux, Barras3F_PV, BarrasConPVs, PoblacionSinOrden)
                fitness = np.zeros((2, individuos))
                for i in range(individuos):
                    fitness[0, i] = -LOSS[i]
                    fitness[1, i] = HCindiv[i]
                poblfinal = poblacion
                from NSGARANK import RANK
                pareto = RANK(fitness)
                from Crowding import Crow
                dst, pareto = Crow(fitness, pareto)
                partfinal = pareto
            from Torneo import tcrz
            R = tcrz(dst, pareto, poblacion, bits, individuos)
            individuos = individuos * 2
            poblacion=R
            if TipoDsimulacion == "ConControlDReg":
                pobaux = poblacion[: , NLL:NLL+PosicionesReg]
                poblacion = poblacion[: , 0:NLL]
            elif TipoDsimulacion == "TotalOpt":
                pobaux = poblacion[: , NLL:NLL + PosicionesReg + CapN + 4 * 2]
                poblacion = poblacion[: , 0:NLL]
            elif TipoDsimulacion == "TotalSinReg":
                pobaux = poblacion[: , NLL:NLL + CapN + 4 * 2]
                poblacion = poblacion[: , 0:NLL]
            if TipoDsimulacion == "ConControlDReg" or TipoDsimulacion == "SinControlDReg" or TipoDsimulacion == "TotalOpt" or TipoDsimulacion == "TotalSinReg" or TipoDsimulacion == "ReconfLocked":
                from radial import rad
                poblacion=rad(poblacion, BusWeight, NB, NLL, individuos, serie)
            if TipoDsimulacion == "ConControlDReg" or TipoDsimulacion == "TotalOpt" or TipoDsimulacion == "TotalSinReg":
                poblacion = np.concatenate((poblacion, pobaux), axis=1)
            R = poblacion
            HCindiv, LOSS, HCindivMenor, LOSSmenor, BarrasConPVs, PoblacionSinOrden = PowerFlow(individuos, NLL, poblacion, NB, NameRegs, Trcontroled, BusDomAleatorio, CantidadInicialPvs, NBC, Semilla, NBCaux, Barras3F_PV, BarrasConPVs, PoblacionSinOrden)
            poblacionMenorLoss = poblacion
            fitness = np.zeros((2, individuos))
            fit_inflexion = np.zeros((2, individuos))
            for i in range(individuos):
                fitness[0, i] = -LOSS[i]
                fitness[1, i] = HCindiv[i]
                fit_inflexion[0, i] = LOSSmenor[i]
                fit_inflexion[1, i] = HCindivMenor[i]
            np.set_printoptions(threshold=sys.maxsize)
            poblfinal = poblacion
            individuos = int(individuos/2)
            from NSGARANK import RANK
            pareto = RANK(fitness)
            from Crowding import Crow
            dst, pareto = Crow(fitness, pareto)
            iaux = 0
            for i in range(1, int(individuos) * 2 + 1):
                for j in range(1, int(individuos) * 2 ):
                    jj = j + 1
                    while jj <= individuos * 2:
                        if pareto[i, j]!=0 and pareto[i, jj]!=0 and iaux < individuos:
                            compara1 = np.equal(R[int(pareto[i, j]-1), :], R[int(pareto[i, jj]-1), :])
                            compara2 = np.all(compara1)
                            if compara2 == 1:
                                pareto[i, jj] = 0
                                iaux = iaux + 1
                        jj = jj + 1

            if TipoDsimulacion == "ConControlDReg":
                poblacion = np.zeros((int(individuos), NLL+PosicionesReg))
            elif TipoDsimulacion == "SinControlDReg" or TipoDsimulacion == "ReconfLocked":
                poblacion = np.zeros((int(individuos), NLL))
            elif TipoDsimulacion == "ConRegSinReconf":
                poblacion = np.zeros((int(individuos), PosicionesReg))
            elif TipoDsimulacion == "BancoCap" or TipoDsimulacion == "BCapLocked":
                poblacion = np.zeros((int(individuos), len(NameCaps)))
            elif TipoDsimulacion == "SoloPV" or TipoDsimulacion == "PVLocked":
                poblacion = np.zeros((int(individuos), 4 * 2))
            elif TipoDsimulacion == "TotalOpt":
                poblacion = np.zeros((int(individuos), NLL + PosicionesReg + CapN + 4 * 2))
            elif TipoDsimulacion == "TotalSinReg":
                poblacion = np.zeros((int(individuos), NLL + CapN + 4 * 2))

            paretoaux = np.zeros((int(individuos)+1, int(individuos)+1))
            dstaux = np.zeros((int(individuos)+1, int(individuos)+1))
            RESPUESTA = np.zeros((2, int(individuos)))
            fitnessaux = np.zeros((2, int(individuos)))
            RESP_inflexion = np.zeros((2, int(individuos)))

            iaux = 1
            for i in range(1, int(individuos * 2 + 1)):
                col = 1
                for j in range(1, int(individuos * 2 + 1)):
                    if i <= individuos and j <= individuos:
                        paretoaux[i, j] = 0
                        dstaux[i, j] = 0
                    if pareto[i, j]!=0 and iaux <= individuos:
                        poblacion[iaux-1,:]=R[int(pareto[i, j]-1),:]
                        paretoaux[i, col] = iaux
                        dstaux[i, col] = dst[i, j]
                        RESPUESTA[0, iaux-1] = fitness[0, int(pareto[i, j]-1)]
                        RESPUESTA[1, iaux-1] = fitness[1, int(pareto[i, j]-1)]
                        fitnessaux[:, iaux-1] = fitness[:, int(pareto[i, j]-1)]
                        RESP_inflexion[0, iaux-1] = -fit_inflexion[0, int(pareto[i, j]-1)]
                        RESP_inflexion[1, iaux-1] = fit_inflexion[1, int(pareto[i, j]-1)]
                        col = col + 1
                        iaux = iaux + 1

            RESPUESTApoblacion = poblacion
            del pareto
            del dst
            del R
            pareto = paretoaux
            dst = dstaux

        np.set_printoptions(threshold=sys.maxsize)
        PoblacionSinOrdenFinal = RESPUESTApoblacion
        BarrasConPVsFinal = BarrasConPVs
        np.set_printoptions(threshold=sys.maxsize)
        Repuesta_Posicion_PVs = np.zeros((2*BarrasConPVsFinal.shape[0], BarrasConPVsFinal.shape[1]))
        for i in range(int(BarrasConPVsFinal.shape[0]/2)):
            for ii in range(RESPUESTA.shape[1]):
                if sum(BarrasConPVsFinal[i * 2 + 1, :]) == RESPUESTA[1, ii]:
                    Repuesta_Posicion_PVs[ii * 2, :] = BarrasConPVsFinal[i * 2, :]
                    Repuesta_Posicion_PVs[ii * 2 + 1, :] = BarrasConPVsFinal[i * 2 + 1, :]

        Ahora = datetime.today()
        Ahora = Ahora.timestamp()
        Ahora = str(Ahora)
        Ahora = Ahora.split(".")
        NombreArchivo = Ahora[0]

        if TipoDsimulacion == "SinControlDReg" or TipoDsimulacion == "ReconfLocked":
            from imprimirSinReg import IMP
            Power, Dsq = IMP(Results_Folder, individuos, pareto, RESPUESTA, NLL, RESPUESTApoblacion, RESP_inflexion, BarrasConPVs, Semilla, NombreArchivo, TipoDsimulacion, iteraciones)
        elif TipoDsimulacion == "ConRegSinReconf":
            from imprimirConRegSinReconf import IMP
            Power, Dsq = IMP(Results_Folder, individuos, pareto, RESPUESTA, PosicionesReg, RESPUESTApoblacion, RESP_inflexion, BarrasConPVs, Semilla, NombreArchivo, TipoDsimulacion, iteraciones)
        elif TipoDsimulacion == "BancoCap" or TipoDsimulacion == "BCapLocked":
            from imprimirCap import IMP
            Power, Dsq = IMP(Results_Folder, individuos, pareto, RESPUESTA, NameCaps, RESPUESTApoblacion, RESP_inflexion, BarrasConPVs, Semilla, NombreArchivo, TipoDsimulacion, iteraciones)
        elif TipoDsimulacion == "SoloPV" or TipoDsimulacion == "PVLocked":
            from imprimirPV import IMP
            Power, Dsq = IMP(Results_Folder, individuos, pareto, RESPUESTA, CtdPV, RESPUESTApoblacion, RESP_inflexion, BarrasConPVs, Semilla, NombreArchivo, TipoDsimulacion, iteraciones)
        if TipoDsimulacion == "TotalOpt":
            from imprimirTotalOpt import IMP
            Power, Dsq = IMP(Results_Folder, individuos, pareto, RESPUESTA, NLL, PosicionesReg, CapN, CtdPV, RESPUESTApoblacion, RESP_inflexion, BarrasConPVs, Semilla, NombreArchivo, TipoDsimulacion, iteraciones)

        end_time = datetime.now()
        print('Duration: {}'.format(end_time - start_time))
        CantidadIter = CantidadIter + 1