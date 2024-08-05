print("not stuck")
import matplotlib.pyplot as plt
import awkward as ak

from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
from coffea.analysis_tools import PackedSelection

import vector as vec
print("not stuck")

from distributed import Client
from lpcjobqueue import LPCCondorCluster

import hist.dask as hda
print("not stuck")

cluster = LPCCondorCluster()
cluster.adapt(minimum=5, maximum=800)
client = Client(cluster)

class ScoutingNanoAODSchema(NanoAODSchema):

    mixins = {
        **NanoAODSchema.mixins,
        "ScoutingJet": "Jet" 
    }
    

# %%
def mass_asymmetry(sj, tj):
    total_p4 = sj[:,0] + sj[:,1] + sj[:,2] + sj[:,3] + sj[:,4] + sj[:,5]
    cart = ak.cartesian([total_p4, tj])
    vector = (cart['1'].j1 + cart['1'].j2 + cart['1'].j3)
    other_vector = (cart['0'] - vector)

    vm = vector.mass
    ovm =other_vector.mass
    masym = (vm - ovm)/(vm + ovm)
    return masym

def tri_mds(tj):
    den=((tj.j1+tj.j2+tj.j3).mass**2)+(tj.j1.mass**2)+(tj.j2.mass**2)+(tj.j3.mass**2)

    m12=((tj.j1+tj.j2).mass**2)/den
    m13=((tj.j1+tj.j3).mass**2)/den
    m23=((tj.j2+tj.j3).mass**2)/den
    #d=ak.zip({"1":m12, "2":m13,"3":m23})
    #d=ak.concatenate([m12[:, np.newaxis], m13[:, np.newaxis],m23[:, np.newaxis]],axis=1)

    r13 = 1/(3**0.5)
    mds=((m12**0.5)-r13)**2 + ((m13**0.5)-r13)**2 + ((m23**0.5)-r13)**2
    #tmds = mds,d[0],d[1],d[2]
    # print(tmds)
    # print(len(tmds))
    return mds, m12, m13, m23

def tri_delta(tj):
    return tj.j1.pt + tj.j2.pt + tj.j3.pt - (tj.j1 + tj.j2 + tj.j3).mass

def tri_mds63(sj, tj):
        total_p4 = sj[:,0] + sj[:,1] + sj[:,2] + sj[:,3] + sj[:,4] + sj[:,5]
        den = 4*total_p4.mass**2 + 6*(sj[:,0].mass**2 + sj[:,1].mass**2  + sj[:,2].mass**2  + sj[:,3].mass**2  + sj[:,4].mass**2  + sj[:,5].mass**2 ) 
        r120 = 1/(20**0.5)
        return ak.sum((((tj.j1 + tj.j2 + tj.j3).mass/den)-r120)**2, axis=1)

def tri_mds6332(sj, tj, mds):
        total_p4 = sj[:,0] + sj[:,1] + sj[:,2] + sj[:,3] + sj[:,4] + sj[:,5]
        den = 4*total_p4.mass**2 + 6*(sj[:,0].mass**2 + sj[:,1].mass**2  + sj[:,2].mass**2  + sj[:,3].mass**2  + sj[:,4].mass**2  + sj[:,5].mass**2 ) 
        r120 = 1/(20**0.5)
        return ak.sum(((((tj.j1 + tj.j2 + tj.j3).mass/den)**2 + mds**0.5)-r120)**2, axis=1)

file_list = [line.strip('\n') for line in open("TTto4Q_TuneCP5_13p6TeV_powheg-pythia8_0000.txt").readlines()] + [line.strip('\n') for line in open("TTto4Q_TuneCP5_13p6TeV_powheg-pythia8_0001.txt").readlines()]
file_list = ["root://cmseos.fnal.gov//" + string for string in file_list]
print("not stuck")

NanoAODSchema.warn_missing_crossrefs = False

small_events = NanoEventsFactory.from_root(
    {file : "Events" for file in file_list},
    schemaclass=ScoutingNanoAODSchema,
    metadata={"dataset": "TTto4Q_TuneCP5_13p6TeV_powheg-pythia8"},
).events()

#uproot.concatenate(file_list)

scouting_selection = PackedSelection()

scouting_selection.add("SixJets", ak.num(small_events.ScoutingJet, axis=1) >5)


good_events = small_events[scouting_selection.all("SixJets")]
selected_jets = good_events.ScoutingJet[:,0:6]
trijet = ak.combinations(selected_jets, 3, fields=["j1","j2","j3"])
print("not stuck")

vec.register_awkward()

mds_val, m12, m13, m23 = tri_mds(trijet)

good_events["Trijet"] = ak.zip(
    {
        "j1": trijet.j1,
        "j2": trijet.j2,
        "j3": trijet.j3,
        "px": trijet.j1.px + trijet.j2.px + trijet.j3.px, 
        "py": trijet.j1.py + trijet.j2.py + trijet.j3.py, 
        "pz": trijet.j1.pz + trijet.j2.pz + trijet.j3.pz,
        "e": trijet.j1.E + trijet.j2.E + trijet.j3.E,
        "masym": mass_asymmetry(selected_jets,trijet),
        "mds": mds_val,
        "m12": m12,
        "m13": m13,
        "m23": m23,
        "delta": tri_delta(trijet),
        "mds63": tri_mds63(selected_jets, trijet),
        "m": (trijet.j1 + trijet.j2 + trijet.j3).mass
        
    },
    with_name="Momentum4D"
)

good_events["HT"] = ak.sum(abs(good_events.ScoutingJet.pt), axis=1)
good_events["mds6332"] = tri_mds6332(selected_jets, trijet, mds_val)




print("Moving to plotting!!")

print(good_events.fields)
print(good_events.Trijet.fields)


print(good_events.Trijet.mass)

# import time
# time.sleep(15)


# exit()

# %%
# h1 = Hist(
#     hist.axis.Regular(50, 0, 3000, name="x", label="HT"),
#     hist.storage.Weight()
# )
# h1.fill(good_events.HT.compute())

# # %%
# h1.plot()
# plt.yscale("log")

# plt.savefig('Run3/HT.png')
# plt.clf()

# print("Next plot")

# # %%
# h2 = Hist(
#     hist.axis.Regular(50, 0, 3600, name="x", label="Jet Pt"),
#     hist.storage.Weight()
# )
# h2.fill(ak.flatten(good_events.ScoutingJet.pt).compute())
# h2.plot()

# plt.savefig('Run3/JetPT.png')
# plt.clf()

# print("Next plot")

# # %%
# h3 = Hist(
#     hist.axis.Regular(50, 0, 1, name="x", label="mds"),
#     hist.storage.Weight()
# )
# h3.fill(ak.flatten(good_events.Trijet.mds.compute()))
# h3.plot()

# plt.savefig('Run3/mds.png')
# plt.clf()

# print("Next plot")

# # %%
# h5 = Hist(
#     hist.axis.Regular(50, -500, 500, name="x", label="delta"),
#     hist.storage.Weight()
# )
# h5.fill(ak.flatten(good_events.Trijet.delta.compute()))
# h5.plot()

# plt.savefig('Run3/delta.png')
# plt.clf()

# print("Next plot")

# # %%
# h6 = Hist(
#     hist.axis.Regular(50, 0, 5, name="x", label="mds6332"),
#     hist.storage.Weight()
# )
# h6.fill(good_events.mds6332.compute())

# # %%
# h6.plot()
# plt.savefig('Run3/mds6332.png')
# plt.clf()

# print("Next plot")


# h4 = Hist(
#     hist.axis.Regular(50, 100, 300, name="x", label="Trijet Invariant Mass"),
#     # hist.axis.StrCategory(['Full', 'Cut'], growth=True, name='dataset'),
#     hist.storage.Weight()
# )
# # h4.fill(ak.flatten(good_events.Trijet.m.compute()), "Full")

# print("here!")
# overallcut = (good_events.mds6332 < 1.25)
# cut_events = good_events[overallcut]
# cut = (cut_events.Trijet.masym < 0.15) & (cut_events.Trijet.mds < 0.175) & (cut_events.Trijet.delta > 250)
# h4.fill(ak.flatten(cut_events.Trijet[cut].m.compute()))
# print("here!")
# h4.plot()

print("here!")
overallcut = (good_events.mds6332 < 1.25) & (good_events.HT > 550)
cut_events = good_events[overallcut]
cut = (cut_events.Trijet.masym < 0.15) & (cut_events.Trijet.mds < 0.175) & (cut_events.Trijet.delta > 250)

print("here!")
dask_hist =  (
    hda.Hist.new.Reg(50, 100, 300, name="inv_mass", label="TTBar Trijet, few selections [GeV]")
    .Double()
    .fill(ak.flatten(cut_events.Trijet.m))
)
print("here!")
dask_hist.compute().plot1d()
print("here!")
plt.savefig('Run3/invmass_3.png')
plt.clf()
print("here!")

# h4[:,"Full"].plot(stack=False, histtype="step")
# plt.legend()

# plt.savefig('Run3/invmass_full.png')
# plt.clf()

print("Done!")

client.close()

