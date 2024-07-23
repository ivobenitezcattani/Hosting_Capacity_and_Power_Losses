def DJ(Llaveamiento, BusWeight, NB, NLL, individuos, serie, LineLengths, objeto):
    import numpy as np
    import sys

    class Graph():
        def __init__(self, nodes):
            self.distArray = [0 for i in range(nodes)]
            self.vistSet = [0 for i in range(nodes)]
            self.V = nodes
            self.INF = 1000000
            self.graph = [[0 for column in range(nodes)]
                          for row in range(nodes)]
        def dijkstra(self, srcNode):
            for i in range(self.V):
                self.distArray[i] = self.INF
                self.vistSet[i] = False
            self.distArray[srcNode] = 0
            for i in range(self.V):
                u = self.minDistance(self.distArray, self.vistSet)
                self.vistSet[u] = True
                for v in range(self.V):
                    if self.graph[u][v] > 0 and self.vistSet[v] == False and self.distArray[v] > self.distArray[u] + \
                            self.graph[u][v]:
                        self.distArray[v] = self.distArray[u] + self.graph[u][v]
        def minDistance(self, distArray, vistSet):
            min = self.INF
            for v in range(self.V):
                if distArray[v] < min and vistSet[v] == False:
                    min = distArray[v]
                    min_index = v
            return min_index
    difx = LineLengths[0, :]
    dify = LineLengths[1, :]
    peso = LineLengths[2, :]
    Busnames = objeto.dssCircuit.AllBusNames
    Apuntador = np.zeros((len(Busnames)))
    for j in range(len(Busnames)):
        Apuntador[j] = j
    Switched_Element = ["" for i in range(NLL)]
    objeto.dssSwitch.First
    for j in range(NLL):
        Switched_Element[j] = objeto.dssSwitch.SwitchedObj
        objeto.dssSwitch.Next
    NombreOriginalLlaves = np.empty([2, NLL], dtype='object')
    for j in range(NLL):
        objeto.dssCircuit.setActiveElement(Switched_Element[j])
        a = objeto.dssLines.Bus1
        b = objeto.dssLines.Bus2
        a = a.split(".")
        a = a[0]
        b = b.split(".")
        b = b[0]
        NombreOriginalLlaves[0, j] = a
        NombreOriginalLlaves[1, j] = b
        for i in range(len(Busnames)):
            if Busnames[i] == a:
                NombreOriginalLlaves[0, j] = Apuntador[i]
            if Busnames[i] == b:
                NombreOriginalLlaves[1, j] = Apuntador[i]
    for j in range(NLL):
        for i in range(NLL):
            if (difx[i] == NombreOriginalLlaves[0, j] and dify[i] == NombreOriginalLlaves[1, j]) or (dify[i] == NombreOriginalLlaves[0, j] and difx[i] == NombreOriginalLlaves[1, j]):
                if Llaveamiento[j] == 0:
                    peso[i] = 999
                else:
                    peso[i] = 0.00001
    np.set_printoptions(threshold=sys.maxsize)
    G = np.zeros((NB, NB))
    for i in range(serie):
        G[int(difx[i]), int(dify[i])] = peso[i]
        G[int(dify[i]), int(difx[i])] = peso[i]
    ourGraph = Graph(NB)
    ourGraph.graph = G
    ourGraph.dijkstra(0)
    distArray = ourGraph.distArray
    return distArray