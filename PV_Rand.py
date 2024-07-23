def PVparameters(objeto, bname, NBCind, Load_fasesInd):
    import numpy as np
    EsteV=4
    kv=4.16 / 1.73
    kva=300
    pmpp=300
    NroFasesConCarga = (int(NBCind[1]))
    if NroFasesConCarga == 1:
        kv = str(kv)
        kv2 = str(0.48/1.73)
    else:
        kv = str(kv * 1.73)
        kv2 = str(0.48)
    for i in range(NroFasesConCarga):
        if i == 0:
            FasesConCarga = str(int(Load_fasesInd[i + 1]))
        else:
            FasesConCarga = FasesConCarga + "." + str(int(Load_fasesInd[i + 1]))
    FasesConCarga = str(FasesConCarga)
    bname = str(bname)
    objeto.dssText.Command = "New line.PV_" + bname + " phases=" + str(int(NBCind[1])) + " bus1=" + bname + "." + FasesConCarga + " bus2=PV_sec_" + bname + "." + FasesConCarga + " switch=yes r1=1e-3 r0=1e-3 x1=0.000 x0=0.000 c1=0.000 c0=0.000 Length=0.001"
    objeto.dssText.Command = "New transformer.PV_" + bname + " phases=" + str(int(NBCind[1])) + " windings=2 buses=(PV_sec_" + bname + "." + FasesConCarga + ", PV_ter_" + bname + "." + FasesConCarga + ") conns=(wye, wye) kVs=(" + kv + " " + kv2 + ") XHL=0.000001 %LoadLoss=0.000001 %R=0.000001 kVAs=(" + str(kva) + ", " + str(kva) + ")"
    objeto.dssText.Command = "makebuslist"
    objeto.dssText.Command = "setkVBase bus=PV_sec_" + bname + " kVLL=4.16"
    objeto.dssText.Command = "setkVBase bus=PV_ter_" + bname + " kVLL=0.48"
    objeto.dssText.Command = "New PVSystem.PV_" + bname + " phases=" + str(int(NBCind[1])) + " conn=wye  bus1=PV_ter_" + bname + "." + FasesConCarga + " kV=" + kv + " kVA=" + str(kva) + " Pmpp=" + str(pmpp) + " %cutin=0.00005 %cutout=0.00005 VarFollowInverter=No vmaxpu=1.3 Temperature=25 irradiance=1"
    objeto.dssText.Command = "New XYcurve.generic npts=5 yarray=[1 1 0 -1 -1] xarray=[0.5 0.92 1.0 1.08 1.5]"
    objeto.dssText.Command = "New XYcurve.NoReactivo npts=3 yarray=[0 0 0] xarray=[0.5 1 1.5]"
    objeto.dssText.Command = "New XYcurve.IEEE1547regA npts=6 yarray=[0.44 0.44 0.001 0.001 -0.44 -0.44] xarray=[0.5 0.92 0.98 1.02 1.08 1.5]"
    objeto.dssText.Command = "New XYcurve.IEEE1547regB npts=6 yarray=[0.4401 0.4401 0.002 0.002 -0.4401 -0.4401] xarray=[0.5 0.95 0.98 1.02 1.05 1.5]"
    objeto.dssText.Command = "New XYcurve.MayorReactivo npts=6 yarray=[0.4402 0.4402 0.003 0.003 -0.4402 -0.4402] xarray=[0.5 0.97 0.99 1.01 1.03 1.5]"
    objeto.dssText.Command = "New InvControl.VoltVar_" + bname + " DERlist=PVSystem.PV_" + bname + " mode=VOLTVAR vvc_curve1=NoReactivo RefReactivePower=VARMAX"
    return EsteV