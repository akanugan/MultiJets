from coffea.nanoevents import NanoEventsFactory, ScoutingNanoAODSchema

from semi_leptonic_top_processor import SemiLeptonicTopProcessor
import dask


file_list = [line.strip('\n') for line in open("filelists/TTto4Q_TuneCP5_13p6TeV_powheg-pythia8_0000.txt").readlines()] + [line.strip('\n') for line in open("filelists/TTto4Q_TuneCP5_13p6TeV_powheg-pythia8_0001.txt").readlines()]
file_list = ["root://cmseos.fnal.gov//" + string for string in file_list]



ScoutingNanoAODSchema.warn_missing_crossrefs = False

small_events = NanoEventsFactory.from_root(
    {file : "Events" for file in file_list[0:5]},
    schemaclass=ScoutingNanoAODSchema,
    metadata={"dataset": "TTto4Q_TuneCP5_13p6TeV_powheg-pythia8"},
).events()

p = SemiLeptonicTopProcessor()

out = p.process(small_events)

(computed,) = dask.compute(out)
print(computed)

