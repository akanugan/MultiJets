import hist
import matplotlib.pyplot as plt
import uproot

from helper_functions import x_sec

file = uproot.open("tight_jet_constraint.root")

a = None
keys = [
"QCD_PT-120to170",
"QCD_PT-170to300",
"QCD_PT-300to470",
"QCD_PT-470to600",
"QCD_PT-600to800",
"QCD_PT-800to1000",
"QCD_PT-1000to1400",
"QCD_PT-1800to2400",
"QCD_PT-1400to1800",
"QCD_PT-2400to3200",
"QCD_PT-3200"]

cats = [
    file["mass/" + "QCD_PT-600to800"].to_hist().axes[0].value(i)
    for i in range(file["mass/" + "QCD_PT-120to170"].to_hist().axes[0].size)
    ]

for cat in cats:

    a = None
    qcd_eff = 0
    total_x = 0

    for key in keys:
        his = file["mass/" + key].to_hist()
        val = float(file["ev/" + key])

        qcd_eff = qcd_eff + (sum(his[cat,:].values()) / val) * x_sec(key)
        total_x = total_x + x_sec(key)

        if a == None:
            a =  his[cat,:] * x_sec(key) / val
        else:
            a = a + his[cat,:] * x_sec(key) / val

    b = file["mass/" + "TTbar"].to_hist()[cat,:] * x_sec("TTto4Q") / float(file["ev/" + "TTbar"])

    h = hist.Stack(a[0:1000:100j],b[0:1000:100j])

    fig, ax = plt.subplots()

    h.plot(stack=True,histtype="fill",label=["QCD","TTBar"])

    qeff = qcd_eff/total_x
    tteff = sum( (file["mass/" + "TTbar"].to_hist()[cat,:].values()) /float(file["ev/" + "TTbar"]))

    plt.text(0.87,0.8,"qcd eff: " + str(round(qeff * 100,3) ) + "%",
             horizontalalignment="center",
            verticalalignment="center",
            transform = ax.transAxes)
    plt.text(0.87,0.7,"tt eff: " + str(round(tteff * 100, 3 ) ) + "%",
             horizontalalignment="center",
            verticalalignment="center",
            transform = ax.transAxes)
    plt.text(0.87,0.6,"Eff ratio = " + str(round(tteff/qeff,3)),
             horizontalalignment="center",
            verticalalignment="center",
            transform = ax.transAxes)
    plt.legend()

    plt.savefig("plots/pruned/mass/" + cat + ".png")

    plt.clf()

    b.plot()

    plt.savefig("plots/pruned/mass/" + cat + "_tt" + ".png")
    plt.clf()

    a = None
    for key in keys:
        his = file["lead_pt/" + key].to_hist() 
        if a == None:
            a =  his[cat,:] * x_sec(key) / float(file["ev/" + key])
        else:
            a = a + his[cat,:] * x_sec(key) / float(file["ev/" + key])


    a[0:500].plot()

    plt.savefig("plots/pruned/pt/" + cat + ".png")
    plt.clf()
