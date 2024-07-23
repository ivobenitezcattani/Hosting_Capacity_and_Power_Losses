def PosicionesDePVs(NBC, Semilla, CantidadInicialPvs):
    import random
    NombreBarrasDom = NBC[0, :]
    NombreBarrasDom = [int(x) for x in NombreBarrasDom]
    NombreBarrasDom = [str(x) for x in NombreBarrasDom]
    random.seed(Semilla)
    BusDomAleatorio = random.sample(NombreBarrasDom, CantidadInicialPvs)
    return BusDomAleatorio