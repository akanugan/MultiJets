import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
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
                'inv_mass_reg4' : {},
                'inv_mass_reg5' : {},
                'inv_mass_reg6' : {}

}

#bins = None

r22 = None

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
    m4 = f['hist_region_4'].to_hist()
    m5 = f['hist_region_5'].to_hist()
    m6 = f['hist_region_6'].to_hist()

    if 'sig' in file:
        if (r22 == None):
            r22 = f['masym_region_2'].to_hist()
            r221 = f['masym_region_1'].to_hist()
            r33 = f['delta_region_3'].to_hist()
            r331 = f['delta_region_1'].to_hist()
            r44 = f['delta phi - pi_region_4'].to_hist()
            r441 = f['delta phi - pi_region_1'].to_hist()
            r55 = f['mds_region_5'].to_hist()
            r551 = f['mds_region_1'].to_hist()
            r66 = f['qgl_region_6'].to_hist()
            r661 = f['qgl_region_1'].to_hist()

            r23 = f['region_2_3'].to_hist()
            r32 = f['region_3_2'].to_hist()
            r24 = f['region_2_4'].to_hist()
            r42 = f['region_4_2'].to_hist()
            r25 = f['region_2_5'].to_hist()
            r52 = f['region_5_2'].to_hist()
            r26 = f['region_2_6'].to_hist()
            r62 = f['region_6_2'].to_hist()
            r34 = f['region_3_4'].to_hist()
            r43 = f['region_4_3'].to_hist()
            r35 = f['region_3_5'].to_hist()
            r53 = f['region_5_3'].to_hist()
            r36 = f['region_3_6'].to_hist()
            r63 = f['region_6_3'].to_hist()
            r45 = f['region_4_5'].to_hist()
            r54 = f['region_5_4'].to_hist()
            r46 = f['region_4_6'].to_hist()
            r64 = f['region_6_4'].to_hist()
            r56 = f['region_5_6'].to_hist()
            r65 = f['region_6_5'].to_hist()
        else:
            r22 = r22 + f['masym_region_2'].to_hist()
            r221 = r221 + f['masym_region_1'].to_hist()
            r33 = r33 + f['delta_region_3'].to_hist()
            r331 = r331 + f['delta_region_1'].to_hist()
            r44 = r44 + f['delta phi - pi_region_4'].to_hist()
            r441 = r441 + f['delta phi - pi_region_1'].to_hist()
            r55 = r55 + f['mds_region_5'].to_hist()
            r551 = r551 + f['mds_region_1'].to_hist()
            r66 = r66 + f['qgl_region_6'].to_hist()
            r661 = r661 + f['qgl_region_1'].to_hist()

            r23 = r23 + f['region_2_3'].to_hist()
            r32 = r32 + f['region_3_2'].to_hist()
            r24 = r24 + f['region_2_4'].to_hist()
            r42 = r42 + f['region_4_2'].to_hist()
            r25 = r25 + f['region_2_5'].to_hist()
            r52 = r52 + f['region_5_2'].to_hist()
            r26 = r26 + f['region_2_6'].to_hist()
            r62 = r62 + f['region_6_2'].to_hist()
            r34 = r34 + f['region_3_4'].to_hist()
            r43 = r43 + f['region_4_3'].to_hist()
            r35 = r35 + f['region_3_5'].to_hist()
            r53 = r53 + f['region_5_3'].to_hist()
            r36 = r36 + f['region_3_6'].to_hist()
            r63 = r63 + f['region_6_3'].to_hist()
            r45 = r45 + f['region_4_5'].to_hist()
            r54 = r54 + f['region_5_4'].to_hist()
            r46 = r46 + f['region_4_6'].to_hist()
            r64 = r64 + f['region_6_4'].to_hist()
            r56 = r56 + f['region_5_6'].to_hist()
            r65 = r65 + f['region_6_5'].to_hist()
    

    histograms['HT'][name] = ht_hist*(weight)
    histograms['inv_mass_reg1'][name] = m1*(weight)
    histograms['inv_mass_reg2'][name] = m2*(weight)
    histograms['inv_mass_reg3'][name] = m3*(weight)
    histograms['inv_mass_reg4'][name] = m4*(weight)
    histograms['inv_mass_reg5'][name] = m5*(weight)
    histograms['inv_mass_reg6'][name] = m6*(weight)
    


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


def plot_inv_mass_region(histograms,region,label):
    inv_mass_hist = sum(histograms[region].values())
    inv_mass_hist.plot()

    plt.xlabel(label)
    #y axis is in pico-barns, need to multiply by luminosity to get num events
    #lum in inverse pico-barns
    plt.savefig("plots/" + region + ".pdf", format="pdf", bbox_inches="tight")
    plt.clf()

    qcd_hists = {k: histograms[region][k] for k in histograms[region].keys() - (histograms[region].keys() - x_sections.keys())}
    sig_hists = {k: histograms[region][k] for k in histograms[region].keys() - x_sections.keys()}


    stack_hist = sum(qcd_hists.values())
    stack_hist.plot()

    for name in sig_hists.keys():
        sig_hists[name].plot(label=name)

    plt.xlabel(label)
    plt.legend()
    plt.savefig("plots/"+region +"_truth.pdf", format="pdf", bbox_inches="tight")
    plt.clf()


# plot_inv_mass_region(histograms,"inv_mass_reg1","Invariant Mass, all pairs [GeV]")
# plot_inv_mass_region(histograms,"inv_mass_reg2","Invariant Mass, Min(masym) [GeV]")
# plot_inv_mass_region(histograms,"inv_mass_reg3","Invariant Mass, Max(delta) [GeV]")
# plot_inv_mass_region(histograms,"inv_mass_reg4","Invariant Mass, Min(delta phi - pi) [GeV]")
# plot_inv_mass_region(histograms,"inv_mass_reg5","Invariant Mass, Min(mds) [GeV]")
# plot_inv_mass_region(histograms,"inv_mass_reg6","Invariant Mass, Max(qgl)->Max(pt) [GeV]")

fig, axs = plt.subplots(5, 5, sharex=False, sharey=False,figsize=(15, 15))

x, y = r22.to_numpy()
y = fix_bins(y)
area = np.trapz(y,x)
x = x / abs(area)
axs[0, 0].plot(y, x)
x, y = r221.to_numpy()
y = fix_bins(y)
area = np.trapz(y,x)
x = x / abs(area)
axs[0, 0].plot(y, x, color='orange')
axs[0,0].set_yticklabels([])

x, y = r33.to_numpy()
y = fix_bins(y)
area = np.trapz(y,x)
x = x / abs(area)
axs[1, 1].plot(y, x)
x, y = r331.to_numpy()
y = fix_bins(y)
area = np.trapz(y,x)
x = x / abs(area)
axs[1, 1].plot(y, x, color='orange')
axs[1, 1].set_yticklabels([])

x, y = r44.to_numpy()
y = fix_bins(y)
area = np.trapz(y,x)
x = x / abs(area)
axs[2, 2].plot(y, x)
x, y = r441.to_numpy()
y = fix_bins(y)
area = np.trapz(y,x)
x = x / abs(area)
axs[2, 2].plot(y, x, color='orange')
axs[2, 2].set_yticklabels([])

x, y = r55.to_numpy()
y = fix_bins(y)
area = np.trapz(y,x)
x = x / abs(area)
axs[3, 3].plot(y, x)
x, y = r551.to_numpy()
y = fix_bins(y)
area = np.trapz(y,x)
x = x / abs(area)
axs[3, 3].plot(y, x, color='orange')
axs[3, 3].set_yticklabels([])

x, y = r66.to_numpy()
y = fix_bins(y)
area = np.trapz(y,x)
x = x / abs(area)
axs[4, 4].plot(y, x)
x, y = r661.to_numpy()
y = fix_bins(y)
area = np.trapz(y,x)
x = x / abs(area)
axs[4, 4].plot(y, x, color='orange')
axs[4, 4].set_yticklabels([])

mynorm = colors.LogNorm()
#mynorm = None

w, x, y = r23.to_numpy()
axs[0, 1].pcolormesh(x, y, w.T,cmap="BuPu",norm= mynorm)
w, x, y = r24.to_numpy()
axs[0, 2].pcolormesh(x, y, w.T,cmap="GnBu",norm= mynorm)
w, x, y = r25.to_numpy()
axs[0, 3].pcolormesh(x, y, w.T,cmap="Blues",norm= mynorm)
w, x, y = r26.to_numpy()
axs[0, 4].pcolormesh(x, y, w.T,cmap="Blues",norm= mynorm)
w, x, y = r32.to_numpy()
axs[1, 0].pcolormesh(x, y, w.T,cmap="YlGn",norm= mynorm)
w, x, y = r34.to_numpy()
axs[1, 2].pcolormesh(x, y, w.T,cmap="PuBuGn",norm= mynorm)
w, x, y = r35.to_numpy()
axs[1, 3].pcolormesh(x, y, w.T,cmap="Blues",norm= mynorm)
w, x, y = r36.to_numpy()
axs[1, 4].pcolormesh(x, y, w.T,cmap="Blues",norm= mynorm)
w, x, y = r42.to_numpy()
axs[2, 0].pcolormesh(x, y, w.T,cmap="OrRd",norm= mynorm)
w, x, y = r43.to_numpy()
axs[2, 1].pcolormesh(x, y, w.T,cmap="BuPu",norm= mynorm)
w, x, y = r45.to_numpy()
axs[2, 3].pcolormesh(x, y, w.T,cmap="Blues",norm= mynorm)
w, x, y = r46.to_numpy()
axs[2, 4].pcolormesh(x, y, w.T,cmap="Blues",norm= mynorm)
w, x, y = r52.to_numpy()
axs[3, 0].pcolormesh(x, y, w.T,cmap="PuBuGn",norm= mynorm)
w, x, y = r53.to_numpy()
axs[3, 1].pcolormesh(x, y, w.T,cmap="OrRd",norm= mynorm)
w, x, y = r54.to_numpy()
axs[3, 2].pcolormesh(x, y, w.T,cmap="Blues",norm= mynorm)
w, x, y = r56.to_numpy()
axs[3, 4].pcolormesh(x, y, w.T,cmap="Blues",norm= mynorm)
w, x, y = r62.to_numpy()
axs[4, 0].pcolormesh(x, y, w.T,cmap="PuBuGn",norm= mynorm)
w, x, y = r63.to_numpy()
axs[4, 1].pcolormesh(x, y, w.T,cmap="OrRd",norm= mynorm)
w, x, y = r64.to_numpy()
axs[4, 2].pcolormesh(x, y, w.T,cmap="Blues",norm= mynorm)
w, x, y = r65.to_numpy()
axs[4, 3].pcolormesh(x, y, w.T,cmap="Blues",norm= mynorm)

axs[0,0].set_title("masym")
axs[0,1].set_title("delta")
axs[0,2].set_title("delta phi - pi")
axs[0,3].set_title("mds")
axs[0,4].set_title("qgl")

axs[0,0].set_ylabel("Min(masym)",rotation=0,size='large')
axs[0,0].yaxis.set_label_coords(-0.39,0.5)
axs[1,0].set_ylabel("Max(delta)",rotation=0,size='large')
axs[1,0].yaxis.set_label_coords(-0.39,0.5)
axs[2,0].set_ylabel("Min(delta phi - pi)",rotation=0,size='large')
axs[2,0].yaxis.set_label_coords(-0.43,0.5)
axs[3,0].set_ylabel("Min(mds)",rotation=0,size='large')
axs[3,0].yaxis.set_label_coords(-0.43,0.5)
axs[4,0].set_ylabel("Max(qgl) \n -> Max(Pt)",rotation=0,size='large')
axs[4,0].yaxis.set_label_coords(-0.43,0.5)

if (mynorm == None):
    plt.savefig("plots/variables.pdf", format="pdf")
else:
    plt.savefig("plots/variables_log.pdf", format="pdf")