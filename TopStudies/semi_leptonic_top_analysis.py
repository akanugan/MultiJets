from coffea.nanoevents import NanoEventsFactory, ScoutingNanoAODSchema

from semi_leptonic_top_processor import SemiLeptonicTopProcessor
import dask

import matplotlib.pyplot as plt

import sys

from distributed import Client
from lpcjobqueue import LPCCondorCluster

cluster = LPCCondorCluster()
cluster.adapt(minimum=1, maximum=2500)
client = Client(cluster)

print("not stuck")


#file_list = [line.strip('\n') for line in open("filelists/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8.txt").readlines()]
file_list = [line.strip('\n') for line in open("filelists/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8_0000.txt").readlines()] + [line.strip('\n') for line in open("filelists/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8_0001.txt").readlines()] + [line.strip('\n') for line in open("filelists/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8_0002.txt").readlines()]
file_list = ["root://cmseos.fnal.gov//" + string for string in file_list]



ScoutingNanoAODSchema.warn_missing_crossrefs = False

small_events = NanoEventsFactory.from_root(
    {file : "Events" for file in file_list},
    schemaclass=ScoutingNanoAODSchema,
    metadata={"dataset": "HadronicTops"},
).events()

p = SemiLeptonicTopProcessor()

out = p.process(small_events)

(computed,) = dask.compute(out)
print(computed)

fig, ax = plt.subplots()
computed["HadronicTops"]["mass"].plot1d(ax=ax)
ax.set_yscale("log")
ax.legend(title="Mass type")

if len(sys.argv) > 1:
    plt.savefig('plots/' + sys.argv[1] + '.png')
else:
    plt.savefig('plots/default.png')

client.close()
