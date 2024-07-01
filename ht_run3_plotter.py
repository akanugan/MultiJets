import matplotlib.pyplot as plt
import argparse
import sys

import uproot

#x-secs times filter eff in picobarns of QCD HT bins
#need to get lowest bin x_sec at some point
x_sections = {
                'QCD_PT-120to170': 445800.0,
                'QCD_PT-170to300': 113700.0,
                'QCD_PT-300to470': 7589.0,
                'QCD_PT-470to600': 626.4,
                'QCD_PT-600to800': 178.6,
                'QCD_PT-800to1000': 30.57,
                'QCD_PT-1000to1400': 8.92,
                'QCD_PT-1400to1800': 0.8103,
                'QCD_PT-1800to2400': 0.1148,
                'QCD_PT-2400to3200': 0.007542,
                'QCD_PT-3200': 0.0002331
}

 

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
        files.append("Run3/mc/QCD/" + line)

HT = []
highest_PT_jet = []

for file in files:
    print("Processing " + file + "...")
    name = QCD_sample_name(file)
    if name is None:
        continue
    f = uproot.open(file)
    br = f['events'].arrays()
    #print(br)
    events = f['cut_flow_hist'].values()[0]
    #print(events)
    #HT.append([br['ak4_HT'], [weights[name] / len(br['ak4_HT'])]* len(br['ak4_HT']),name])
    #print((x_sections[name] / events)* len(br['event_HT']))

    HT.append([br['event_HT'], [x_sections[name] / events]* len(br['event_HT']),name])
    highest_PT_jet.append([br['ak4_pt'][:,0], [x_sections[name] / events]* len(br['ak4_pt'][:,0]),name])

print("Plotting...")
plt.hist([row[0] for row in HT], weights= [row[1] for row in HT], bins= 100,stacked=True,label=[row[2] for row in HT],range=(0,14000))
plt.xlabel("HT [GeV]")
#y axis is in pico-barns, need to multiply by luminosity to get num events
#lum in inverse pico-barns
plt.yscale('log')

plt.legend()
plt.savefig("run3_plots/HT.pdf", format="pdf")



plt.clf()
plt.hist([row[0] for row in highest_PT_jet], weights= [row[1] for row in highest_PT_jet], bins= 100,stacked=True,label=[row[2] for row in highest_PT_jet],range=(0,4000))
plt.xlabel("pt [GeV]")

#y axis is in pico-barns, need to multiply by luminosity to get num events
#lum in inverse pico-barns
plt.yscale('log')
plt.legend()
plt.savefig("run3_plots/pt.pdf", format="pdf")
