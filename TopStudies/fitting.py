"""Testing out fitting methods."""

import matplotlib.pyplot as plt
import uproot
import zfit

file = uproot.open("truth_trial.root")

h = file["mass"].to_hist()
h = h["w",:]


binned_data = zfit.data.BinnedData.from_hist(h)

binning = zfit.binned.RegularBinning(120, 60, 120, name="mass")
space = zfit.Space("mass", binning=binning)

background = zfit.Parameter("background", 0)
mu = zfit.Parameter("mu", 80)
gamma = zfit.Parameter("gamma", 4)
unbinned_model = zfit.pdf.SumPDF(
    [zfit.pdf.Uniform(60, 120, space), zfit.pdf.Cauchy(mu, gamma, space)], [background],
)

model = zfit.pdf.BinnedFromUnbinnedPDF(unbinned_model, space)
loss = zfit.loss.BinnedNLL(model, binned_data)

minimizer = zfit.minimize.Minuit()
result = minimizer.minimize(loss)

binned_data.to_hist().plot(density=1)
model.to_hist().plot(density=1)


plt.savefig("tester_mass_lin.png")


