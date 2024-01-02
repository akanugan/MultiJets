import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import hist
import argparse

import uproot
import awkward as awk

#x-secs times filter eff in picobarns of QCD HT bins
#need to get lowest bin x_sec at some point
x_sections = {'QCD_HT300to500': 0,
            'QCD_HT500to700': 29370,
            'QCD_HT700to1000': 6524,
            'QCD_HT1000to1500': 1064,
            'QCD_HT1500to2000': 121.5,
            'QCD_HT2000toInf': 25.42
}            

def fix_bins(bins):
    arr = []
    #uproot delivers the bins in an array that 
    # has one more element than the total number of bins
    #This sets each value in the middle of the bin
    #so the length of the array matches the number of bins
    for i in range(0, len(bins)-1):
        arr.append(round((bins[i+1]-bins[i])/2+bins[i],2))
    return arr

def QCD_sample_name(name):
    for key in x_sections.keys():
        if key in name:
            return key
    return None


oldargv = sys.argv[:]
sys.argv = [ '-b-' ]
sys.argv = oldargv
parser = argparse.ArgumentParser()
parser.add_argument("inFile", help="Location of input file/files")
args = parser.parse_args()


files = []
with open(args.inFile,'r') as file_list:
    for line in file_list:
        line = line.strip()
        files.append(line)

#Dictionary of all histograms to be made
histograms = {
                'HT' : {},
                'inv_mass_reg1' : {},
                'inv_mass_reg2' : {},
                'inv_mass_reg3' : {},
}

#bins = None

for file in files:
    
    print("Processing " + file + "...")
    name = QCD_sample_name(file)
        
    if name is None:
        if 'sig' in file:
            name = file.split('.',1)[0].split("/",1)[1]
            weight = 0.00005
        else:
            continue

    f = uproot.open(file)
    if name in x_sections.keys():
        events = f['cut_flow_hist'].values()[0]
        weight = x_sections[name] / events


    ht_hist = f['ht_plot'].to_hist()
    m1 = f['hist_region_1'].to_hist()
    m2 = f['hist_region_2'].to_hist()
    m3 = f['hist_region_3'].to_hist()

    histograms['HT'][name] = ht_hist*(weight)
    histograms['inv_mass_reg1'][name] = m1*(weight)
    histograms['inv_mass_reg2'][name] = m2*(weight)
    histograms['inv_mass_reg3'][name] = m3*(weight)
    


print("Plotting...")



qcd_hists = {k: histograms['HT'][k] for k in histograms['HT'].keys() - (histograms['HT'].keys() - x_sections.keys())}
sig_hists = {k: histograms['HT'][k] for k in histograms['HT'].keys() - x_sections.keys()}


stack_hist = hist.Stack.from_dict(qcd_hists)
stack_hist.plot(stack = True,histtype="fill")

for name in sig_hists.keys():
    sig_hists[name].plot(label=name)



plt.xlabel("HT [GeV]")
plt.xlim(550,3000)
#y axis is in pico-barns, need to multiply by luminosity to get num events
#lum in inverse pico-barns
plt.yscale('log')
plt.legend()
plt.savefig("plots/HT.pdf", format="pdf", bbox_inches="tight")
plt.clf()

inv_mass_hist = sum(histograms['inv_mass_reg1'].values())
inv_mass_hist.plot()

plt.xlabel("Invariant Mass, all pairs [GeV]")
#y axis is in pico-barns, need to multiply by luminosity to get num events
#lum in inverse pico-barns
plt.savefig("plots/inv_mass_reg1.pdf", format="pdf", bbox_inches="tight")
plt.clf()

inv_mass_hist = sum(histograms['inv_mass_reg2'].values())
inv_mass_hist.plot()

plt.xlabel("Invariant Mas, lowest asymmetry pair kept [GeV]")
#y axis is in pico-barns, need to multiply by luminosity to get num events
#lum in inverse pico-barns
plt.savefig("plots/inv_mass_reg2.pdf", format="pdf", bbox_inches="tight")
plt.clf()

inv_mass_hist = sum(histograms['inv_mass_reg3'].values())
inv_mass_hist.plot()

plt.xlabel("Invariant Mass [GeV]")
#y axis is in pico-barns, need to multiply by luminosity to get num events
#lum in inverse pico-barns
plt.savefig("plots/inv_mass_reg3.pdf", format="pdf", bbox_inches="tight")
plt.clf()

qcd_hists = {k: histograms['inv_mass_reg1'][k] for k in histograms['inv_mass_reg1'].keys() - (histograms['inv_mass_reg1'].keys() - x_sections.keys())}
sig_hists = {k: histograms['inv_mass_reg1'][k] for k in histograms['inv_mass_reg1'].keys() - x_sections.keys()}


stack_hist = sum(qcd_hists.values())
stack_hist.plot()

for name in sig_hists.keys():
    sig_hists[name].plot(label=name)

plt.xlabel("Invariant Mass [GeV]")
#y axis is in pico-barns, need to multiply by luminosity to get num events
#lum in inverse pico-barns
plt.legend()
plt.savefig("plots/inv_mass_reg1_truth.pdf", format="pdf", bbox_inches="tight")
plt.clf()

qcd_hists = {k: histograms['inv_mass_reg2'][k] for k in histograms['inv_mass_reg2'].keys() - (histograms['inv_mass_reg2'].keys() - x_sections.keys())}
sig_hists = {k: histograms['inv_mass_reg2'][k] for k in histograms['inv_mass_reg2'].keys() - x_sections.keys()}


stack_hist = sum(qcd_hists.values())
stack_hist.plot()

for name in sig_hists.keys():
    sig_hists[name].plot(label=name)

plt.xlabel("Invariant Mass [GeV]")
#y axis is in pico-barns, need to multiply by luminosity to get num events
#lum in inverse pico-barns
plt.legend()
plt.savefig("plots/inv_mass_reg2_truth.pdf", format="pdf", bbox_inches="tight")
plt.clf()

qcd_hists = {k: histograms['inv_mass_reg3'][k] for k in histograms['inv_mass_reg3'].keys() - (histograms['inv_mass_reg3'].keys() - x_sections.keys())}
sig_hists = {k: histograms['inv_mass_reg3'][k] for k in histograms['inv_mass_reg3'].keys() - x_sections.keys()}


stack_hist = sum(qcd_hists.values())
stack_hist.plot()

for name in sig_hists.keys():
    sig_hists[name].plot(label=name)

plt.xlabel("Invariant Mass [GeV]")
#y axis is in pico-barns, need to multiply by luminosity to get num events
#lum in inverse pico-barns
plt.legend()
plt.savefig("plots/inv_mass_reg3_truth.pdf", format="pdf", bbox_inches="tight")
plt.clf()