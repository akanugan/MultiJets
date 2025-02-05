
import ctypes

import ROOT

from helper_functions import get_QCD_keys, x_sec

top = {}
qcd = {}

with ROOT.TFile.Open("tight_jet_constraint.root","READ") as mc_file:

    temp_h = mc_file.mass.Get("TTbar")
    bin_sel = temp_h.GetXaxis().FindBin("Full")
    top["TTto4Q"] = {
        "hist": temp_h.ProjectionY("Full",bin_sel,bin_sel),
        "weight": x_sec("TTto4Q") / mc_file.ev.Get("TTbar").GetString().Atof(),
    }
    top["TTto4Q"]["hist"].SetDirectory(ROOT.nullptr)

    for key in get_QCD_keys():

        temp_h = mc_file.mass.Get(key)
        bin_sel = temp_h.GetXaxis().FindBin("Full")

        qcd[key] = {
            "hist": temp_h.ProjectionY("Full",bin_sel,bin_sel),
            "weight": x_sec(key) / mc_file.ev.Get(key).GetString().Atof(),
                    }
        qcd[key]["hist"].SetDirectory(ROOT.nullptr)

qcd_hist = None

for sec in qcd:

    if qcd_hist is None:
        qcd_hist = qcd[sec]["hist"] * qcd[sec]["weight"]
    else:
        qcd_hist = qcd_hist + qcd[sec]["hist"] * qcd[sec]["weight"]

data_dict = {}

with ROOT.TFile.Open("data_test.root","READ") as data_file:
    temp_h = data_file.mass.Get("Run2022F_360335-360941_0002")
    bin_sel = temp_h.GetXaxis().FindBin("Full")

    data_dict["hist"] = temp_h.ProjectionY("Full",bin_sel,bin_sel)

    data_dict["hist"].SetDirectory(ROOT.nullptr)


data = data_dict["hist"]

data.Rebin(40)
qcd_hist.Rebin(40)

data_norm = data.Integral()
qcd_norm = qcd_hist.Integral()

qcd_hist = (data_norm/qcd_norm)*qcd_hist

c1 = ROOT.TCanvas()
qcd_hist.Draw("HIST")
data.Draw("same ep")

legend = ROOT.TLegend()
legend.AddEntry(data, "data","ep")
legend.AddEntry(qcd_hist, "QCD","")
legend.Draw("same")


with ROOT.TFile("data_fit_1_hists.root", "recreate") as outfile:
    outfile.WriteObject(qcd_hist, "qcd")
    outfile.WriteObject(data, "data")
    outfile.WriteObject(c1,"canvas")
