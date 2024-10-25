"""Testing out fitting methods."""
import ctypes

import ROOT

from helper_functions import get_QCD_keys, x_sec

top = {}
qcd = {}

with ROOT.TFile.Open("tight_jet_constraint.root","READ") as mc_file:

    temp_h = mc_file.mass.Get("TTbar")
    bin_sel = temp_h.GetXaxis().FindBin("DeltaGr250")
    top["TTto4Q"] = {
        "hist": temp_h.ProjectionY("DGr250",bin_sel,bin_sel),
        "weight": x_sec("TTto4Q") / mc_file.ev.Get("TTbar").GetString().Atof(),
    }
    top["TTto4Q"]["hist"].SetDirectory(ROOT.nullptr)

    for key in get_QCD_keys():

        temp_h = mc_file.mass.Get(key)
        bin_sel = temp_h.GetXaxis().FindBin("DeltaGr250")

        qcd[key] = {
            "hist": temp_h.ProjectionY("DGr250",bin_sel,bin_sel),
            "weight": x_sec(key) / mc_file.ev.Get(key).GetString().Atof(),
                    }
        qcd[key]["hist"].SetDirectory(ROOT.nullptr)

qcd_hist = None

for sec in qcd:

    if qcd_hist is None:
        qcd_hist = qcd[sec]["hist"] * qcd[sec]["weight"]
    else:
        qcd_hist = qcd_hist + qcd[sec]["hist"] * qcd[sec]["weight"]

top_hist = top["TTto4Q"]["hist"] * top["TTto4Q"]["weight"]
qcd_hist.Rebin(20)
top_hist.Rebin(20)

print(qcd_hist)

top_mod = 1
fake_data = (qcd_hist + top_mod * top_hist)

# fake_data = ROOT.TH1F("fake_data","fake_data",50,100,300)
# rand = ROOT.TRandom3(451)
# fake_data.FillRandom(fake_data_profile,10_000_000,rand)

# norm = fake_data_profile.Integral() / fake_data.Integral()
# print(norm)
# fake_data.Scale(norm)

mc = ROOT.TObjArray(2)

mc.Add(qcd_hist)
mc.Add(top_hist)

fit = ROOT.TFractionFitter(fake_data,mc)

fit.SetRangeX(100,300)

status = fit.Fit()
result = fit.GetPlot()

qcd_frac, qcd_error = ctypes.c_double(0.),ctypes.c_double(0.)
top_frac, top_error = ctypes.c_double(0.),ctypes.c_double(0.)
fit.GetResult(0,qcd_frac, qcd_error)
fit.GetResult(1,top_frac, top_error)
tot_norm = result.Integral()
qcd_norm = qcd_hist.Integral()
top_norm = top_hist.Integral()
comb_norm = qcd_norm + top_mod*top_norm
print("QCD norm: " + str(qcd_norm) + " divided by tot_norm: "  + str(qcd_norm/(comb_norm)))
print("Top norm: " + str(top_mod*top_norm) + " divided by tot_norm: "  + str(top_mod*top_norm/(comb_norm)))

qcd_result = qcd_frac.value*(tot_norm/qcd_norm)*qcd_hist
top_result = top_frac.value*(tot_norm/top_norm)*top_hist

result_2 = qcd_result + top_result

c1 = ROOT.TCanvas()
fake_data.Draw("ep")

result.SetLineColor(ROOT.kGreen)
result.Draw("same F")
result_2.SetLineColor(ROOT.kRed)
result_2.Draw("same")
qcd_result.SetLineColor(2)
qcd_result.Draw("same L")
qcd_result.SetLineColor(3)
top_result.Draw("same L")

legend = ROOT.TLegend()
legend.AddEntry(fake_data, "QCD + n*Top from MC","ep")
legend.AddEntry(result, "Total Fit result","l")
legend.AddEntry(result_2, "Added QCD + ttbar","")
legend.AddEntry(qcd_result, "QCD","")
legend.AddEntry(top_result, "TTbar","")
legend.Draw("same")


with ROOT.TFile("fit_6_hists.root", "recreate") as outfile:
    outfile.WriteObject(qcd_hist, "qcd")
    outfile.WriteObject(top_hist, "top")
    outfile.WriteObject(fake_data, "fake_data")
    outfile.WriteObject(result, "fit_result")
    outfile.WriteObject(c1,"canvas")

