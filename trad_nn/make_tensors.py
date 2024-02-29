import torch
import numpy as np
import uproot
#import pandas as pd

tree = uproot.open("/uscms/home/jlawless/nobackup/MultiJets/full_ntuples/slimmedNtup_gl1750.root")["events"]

phi = tree["jtrip_phi"].array()
delta = tree["jtrip_delta"].array()
masym = tree["jtrip_masym"].array()
qgl = tree["jtrip_qgl"].array()
mds = tree["jtrip_mds"].array()

mass = tree["jtrip_mass"].array()

match = tree["jtrip_match"].array()

events = []

print("Processing " + str(len(mass)) + " events...")

for j in range(len(mass)):
    event = []

    if j % 500 == 0:
        print(str(j) + "...")
    
    no_signal = True
    for i in range(10):
        #make one entry per triplet pair
        tp = []
        #only need one mass asymmetry per pair, since it should be the same
        tp.append(masym[j][2*i])

        tp.append(delta[j][2*i])
        tp.append(delta[j][2*i + 1])

        #calculate the delta phi and give them that
        tp.append(phi[j][2*i+1] - phi[j][2*i] - 3.1415)

        tp.append(mds[j][2*i])
        tp.append(mds[j][2*i + 1])

        tp.append(qgl[j][2*i])
        tp.append(qgl[j][2*i + 1])

        

        #its only signal if both are signal
        if(match[j][2*i] != 0 and match[j][2*i + 1] != 0):
            no_signal = False
            tp.append(1)
        else:
            tp.append(0)

        tp.append(mass[j][2*i])
        tp.append(mass[j][2*i + 1])
        

        event.append(tp)

    #only keep events that have a signal in them
    if(no_signal):
        continue
    events.append(event)

print(len(events))



data = np.array(events)

X = np.array([i.flatten() for i in data[:,:,0:8]])
Y = data[:,:,8]
M = data[:,:,9:]

X = torch.tensor(X, dtype=torch.float32)
Y = torch.tensor(Y, dtype=torch.float32)
M = torch.tensor(M, dtype=torch.float32)

torch.save(X,'x_1750_tensor.pd')
torch.save(Y,'y_1750_tensor.pd')
torch.save(M,'m_1750_tensor.pd')

