import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import uproot
import awkward as awk

files = []
with open('file_list.txt','r') as file_list:
    for line in file_list:
        line = line.strip().split(' ')
        files.append(line)

weights = {'QCD_HT300to500': 5.840092228107049,
            'QCD_HT500to700': 0.5645990685276228 ,
            'QCD_HT700to1000': 0.15253309779537536 ,
            'QCD_HT1000to1500': 0.07186338787825997 ,
            'QCD_HT1500to2000': 0.010317626274751761 ,
            'QCD_HT2000toInf': 0.004261168431292373
            }
HT = []

for file in files:
    f = uproot.open('output2/' + file[1])
    br = f['events'].arrays()
    HT.append([br['ak4_HT'], [weights[file[0]]]* len(br['ak4_HT']),file[0]])
 
print(HT)
plt.hist([row[0] for row in HT], weights= [row[1] for row in HT], bins= 100,stacked=True,label=[row[2] for row in HT],range=(0,3000))
plt.xlabel("HT [GeV]")
plt.legend()
plt.show()
