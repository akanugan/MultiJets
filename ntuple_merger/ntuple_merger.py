import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import uproot
import awkward as awk

weights = {'QCD_HT300to500': 5.840092228107049,
            'QCD_HT500to700': 0.5645990685276228 ,
            'QCD_HT700to1000': 0.15253309779537536 ,
            'QCD_HT1000to1500': 0.07186338787825997 ,
            'QCD_HT1500to2000': 0.010317626274751761 ,
            'QCD_HT2000toInf': 0.004261168431292373
            }
def QCD_sample_name(name):
    for key in weights.keys():
        if key in name:
            return key
    return None


files = []
with open('file_list.txt','r') as file_list:
    for line in file_list:
        line = line.strip()
        files.append(line)

HT = []

for file in files:
    print("Processing " + file + "...")
    name = QCD_sample_name(file)
    if name is None:
        continue
    f = uproot.open('../slimmed_ntuples/' + file)
    br = f['events'].arrays()
    events = f['cut_flow_hist'].values()[0]
    #HT.append([br['ak4_HT'], [weights[name] / len(br['ak4_HT'])]* len(br['ak4_HT']),name])
    HT.append([br['ak4_HT'], [weights[name] / events]* len(br['ak4_HT']),name])

print("Plotting...")
plt.hist([row[0] for row in HT], weights= [row[1] for row in HT], bins= 100,stacked=True,label=[row[2] for row in HT],range=(0,3000))
plt.xlabel("HT [GeV]")
plt.yscale('log')
plt.legend()
plt.show()
