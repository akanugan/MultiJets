import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

 

def QCD_sample_name(name):
    for key in x_sections.keys():
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
    HT.append([br['ak4_HT'], [x_sections[name] / events]* len(br['ak4_HT']),name])

print("Plotting...")
plt.hist([row[0] for row in HT], weights= [row[1] for row in HT], bins= 100,stacked=True,label=[row[2] for row in HT],range=(0,3000))
plt.xlabel("HT [GeV]")
#y axis is in pico-barns, need to multiply by luminosity to get num events
#lum in inverse pico-barns
plt.yscale('log')
plt.legend()
plt.show()
