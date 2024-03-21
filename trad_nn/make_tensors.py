import os
import argparse

import torch
import numpy as np
import uproot

import variable_input as vin

parser = argparse.ArgumentParser(description="Processes the root file into the tensor format needed for the Neural Network.")
parser.add_argument("inFile", help="Location of input file/files")
parser.add_argument('-t',"--title", help="Title for the directory", default="nn")
args = parser.parse_args()

os.mkdir(args.title)
os.mkdir(args.title + "/plots")

print(torch.cuda.is_available())


tree = uproot.open(args.inFile)["events"]

functions = vin.input_dict()

variables = {}
for key in functions.keys():
    variables[key] = tree[key].array()


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

        for key in variables.keys():
            functions[key](tp,variables[key],j,i)

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

data = np.array(events)

X = np.array([i.flatten() for i in data[:,:,0:-3]])
Y = data[:,:,-3]
M = data[:,:,-2:]

X = torch.tensor(X, dtype=torch.float32)
Y = torch.tensor(Y, dtype=torch.float32)
M = torch.tensor(M, dtype=torch.float32)

torch.save(X,args.title +'/x_tensor.pd')
torch.save(Y,args.title +'/y_tensor.pd')
torch.save(M,args.title +'/m_tensor.pd')


f = open(args.title + "/model_info.txt", "w")
f.write("Processed " + str(len(mass)) + " events, kept " + str(len(data)) + "\n \n")

f.write("Using inputs: \n")
for key in functions.keys():
    f.write("   -" + key)
    f.write('\n')
f.write('\n')
f.close()
