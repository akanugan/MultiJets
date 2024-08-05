# %%
import matplotlib.pyplot as plt
import awkward as ak
import numpy as np

from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
from coffea.analysis_tools import PackedSelection

import hist
from hist import Hist
import hist.dask as hda

import vector as vec

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
                'QCD_PT-3200': 0.0002331,
                'TTto4Q': 762.1
}

 

def sample_name(name):
    for key in x_sections.keys():
        if key in name:
            return key
    return None

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


# %%
file_list = [line.strip('\n') for line in open("TTto4Q_TuneCP5_13p6TeV_powheg-pythia8_0000.txt").readlines()] + [line.strip('\n') for line in open("TTto4Q_TuneCP5_13p6TeV_powheg-pythia8_0001.txt").readlines()]
file_list = ["root://cmseos.fnal.gov//" + string for string in file_list]

NanoAODSchema.warn_missing_crossrefs = False

events = NanoEventsFactory.from_root(
    {file : "Events" for file in file_list},
    schemaclass=ScoutingNanoAODSchema,
    metadata={"dataset": "TTto4Q_TuneCP5_13p6TeV_powheg-pythia8"},
).events()

small_events = NanoEventsFactory.from_root(
    {file : "Events" for file in file_list[0:2]},
    schemaclass=ScoutingNanoAODSchema,
    metadata={"dataset": "TTto4Q_TuneCP5_13p6TeV_powheg-pythia8"},
).events()

qcd_events = {}

for f in [line.strip('\n') for line in open("qcd_files.txt").readlines()]:
    file_list = [line.strip('\n') for line in open(f).readlines()]
    file_list = ["root://cmseos.fnal.gov//" + string for string in file_list]
    qcd_events[sample_name(f)] = NanoEventsFactory.from_root(
        {file : "Events" for file in file_list[0:2]},
        schemaclass=ScoutingNanoAODSchema,
        metadata={"dataset": sample_name(f)},
        ).events()
    
    #num_events = ak.num(qcd_events[sample_name(f)],axis=0).compute()
    #qcd_events[sample_name(f)]["Weight"] = dak.Array(np.full(num_events,(x_sections[sample_name(f)] / num_events)))

# dask_hist =  (
#     hda.Hist.new.Reg(60, 0, 6000, name="jet pt", label="Jet pt [GeV]")
#     .StrCat(x_sections.keys(), name='dataset')
#     .Weight()
# )

# for ky in x_sections.keys():
#     if ky not in ['TTto4Q']:
#         dask_hist.fill(ak.drop_none(ak.max(qcd_events[ky].ScoutingJet.pt,axis=1)), ky, weight=(x_sections[ky] / (ak.num(qcd_events[ky], axis=0))))

# dask_hist.compute().plot1d(stack=True,histtype="fill")
# plt.yscale('log')
# plt.legend()

# # %%
# dask_hist =  (
#     hda.Hist.new.Reg(50, 20, 2000, name="jet pt", label="Jet pt [GeV]")
#     .Weight()
#     .fill(ak.drop_none(qcd_events['QCD_PT-1000to1400'].ScoutingJet)[:,0].pt, weight=1)
# )

# dask_hist.compute().plot1d()
# plt.yscale('log')

vec.register_awkward()

def format_good_events(ev):
    sel = PackedSelection()
    sel.add("SixJets", ak.num(ev.ScoutingJet, axis=1) >5)

    result = ev[sel.all("SixJets")]
    selected_jets = result.ScoutingJet[:,0:6]
    trijet = ak.combinations(selected_jets, 3, fields=["j1","j2","j3"])

    mds_val, m12, m13, m23 = tri_mds(trijet)

    result["Trijet"] = ak.zip(
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

    result["HT"] = ak.sum(abs(result.ScoutingJet.pt), axis=1)
    result["mds6332"] = tri_mds6332(selected_jets, trijet, mds_val)

    return result

good_qcd_events = {}

for key in x_sections.keys():
    if key not in ['TTto4Q']:
        good_qcd_events[key] = format_good_events(qcd_events[key])

good_events = format_good_events(small_events)

# h1 = Hist(
#     hist.axis.Regular(50, 0, 3000, name="x", label="HT"),
#     hist.storage.Weight()
# )
# h1.fill(good_events.HT.compute())

# dask_hist_HT =  (
#     hda.Hist.new.Reg(60, 0, 6000, name="ht", label="HT [GeV]")
#     .StrCat(x_sections.keys(), name='dataset')
#     .Weight()
# )

# for ky in x_sections.keys():
#     if ky not in ['TTto4Q']:
#         dask_hist_HT.fill(good_qcd_events[ky].HT, ky, weight=(x_sections[ky] / (ak.num(qcd_events[ky], axis=0))))

# dask_hist_HT.fill(good_events.HT, 'TTto4Q', weight=(x_sections['TTto4Q'] / (ak.num(small_events, axis=0))))

# dask_hist_HT.compute().plot1d(stack=True,histtype="fill")

# plt.yscale("log")
# plt.legend()

# h1.plot()
# plt.yscale("log")

# # %%
# h2 = Hist(
#     hist.axis.Regular(50, 0, 3600, name="x", label="Jet Pt"),
#     hist.storage.Weight()
# )
# h2.fill(ak.flatten(good_events.ScoutingJet.pt).compute())

# # %%
# good_events.Trijet.fields

# # %%
# h3 = Hist(
#     hist.axis.Regular(50, 0, 1, name="x", label="mds"),
#     hist.storage.Weight()
# )
# h3.fill(ak.flatten(good_events.Trijet.mds.compute()))

# # %%
# h5 = Hist(
#     hist.axis.Regular(50, -500, 500, name="x", label="delta"),
#     hist.storage.Weight()
# )
# h5.fill(ak.flatten(good_events.Trijet.delta.compute()))

# # %%
# h6 = Hist(
#     hist.axis.Regular(50, 0, 5, name="x", label="mds6332"),
#     hist.storage.Weight()
# )
# h6.fill(good_events.mds6332.compute())

# # %%
# h6.plot()

# # %%
# h4 = Hist(
#     hist.axis.Regular(50, 100, 300, name="x", label="Trijet Invariant Mass"),
#     hist.axis.StrCategory(['Full'], growth=True, name='dataset'),
#     hist.storage.Weight()
# )
# h4.fill(ak.flatten(good_events.Trijet.mass.compute()), "Full")
# overallcut = (good_events.HT > 550)
# cut_events = good_events[overallcut]
# cut = (cut_events.Trijet.masym < 0.15) & (cut_events.Trijet.mds < 0.175) #& (cut_events.Trijet.delta > 250)
# h4.fill(ak.flatten(cut_events.Trijet[cut].mass.compute()), "CutNoDelta")
# cut = (cut_events.Trijet.masym < 0.15) & (cut_events.Trijet.mds < 0.175) & (cut_events.Trijet.delta > 0)
# h4.fill(ak.flatten(cut_events.Trijet[cut].mass.compute()), "DeltaGr0")
# cut = (cut_events.Trijet.masym < 0.15) & (cut_events.Trijet.mds < 0.175) & (cut_events.Trijet.delta > 125)
# h4.fill(ak.flatten(cut_events.Trijet[cut].mass.compute()), "DeltaGr125")
# cut = (cut_events.Trijet.masym < 0.15) & (cut_events.Trijet.mds < 0.175) & (cut_events.Trijet.delta > 250)
# h4.fill(ak.flatten(cut_events.Trijet[cut].mass.compute()), "DeltaGr250")
# cut_events = good_events #[overallcut]
# cut = ak.argmin(cut_events.Trijet.masym,axis=1,keepdims=True)
# h4.fill(ak.flatten(cut_events.Trijet[cut].mass).compute(), "MinAsy")


# # %%
# h4.plot(stack=False, histtype="step")
# plt.yscale("log")
# plt.legend(loc="upper right")

# # %%
# h4[:,""].plot(stack=False, histtype="step")
# plt.legend(loc="upper right")

# # %%
# h4[:,["DeltaGr125","DeltaGr0","DeltaGr250"]].plot(stack=False, histtype="step")
# plt.yscale("log")
# plt.legend()

# # %%
# h4 = Hist(
#     hist.axis.Regular(50, 100, 300, name="x", label="Trijet Invariant Mass"),
#     hist.axis.StrCategory(['Full', 'Cut'], growth=True, name='dataset'),
#     hist.storage.Weight()
# )
# h4.fill(ak.flatten(good_events.Trijet.mass.compute()), "Full")
# overallcut = (good_events.mds6332 < 1.25)
# cut_events = good_events[overallcut]
# cut = (cut_events.Trijet.masym < 0.15) & (cut_events.Trijet.mds < 0.175) & (cut_events.Trijet.delta > 250)

# # %%
# dask_hist =  (
#     hda.Hist.new.Reg(50, 100, 300, name="inv_mass", label="TTBar Trijet, with selections [GeV]")
#     .Double()
#     .fill(ak.flatten(cut_events.Trijet[cut].mass))
# )

# # %%
# dask_hist.compute().plot1d()

# %%
dask_hist_mass =  (
    hda.Hist.new.Reg(60, 0, 6000, name="mass", label="Invariant Mass [GeV]")
    #.StrCat(['FullQCD','MinAsyQCD'], name='dataset')
    .Weight()
)
for key in x_sections.keys():
    if key not in ['TTto4Q']:
        dask_hist_mass.fill(ak.flatten(good_qcd_events[key].Trijet.m), weight=(x_sections[key] / (ak.num(qcd_events[key], axis=0).compute())))
        # overallcut = (good_qcd_events[key].HT > 550)
        # cut_events = good_qcd_events[key][overallcut]
        # cut = (cut_events.Trijet.masym < 0.15) & (cut_events.Trijet.mds < 0.175) #& (cut_events.Trijet.delta > 250)
        # dask_hist_mass.fill(ak.flatten(cut_events.Trijet[cut].mass), "CutNoDeltaQCD",weight=(x_sections[key] / (ak.num(qcd_events[key], axis=0)))
        # cut = (cut_events.Trijet.masym < 0.15) & (cut_events.Trijet.mds < 0.175) & (cut_events.Trijet.delta > 0)
        # dask_hist_mass.fill(ak.flatten(cut_events.Trijet[cut].mass), "DeltaGr0QCD",weight=(x_sections[key] / (ak.num(qcd_events[key], axis=0)))
        # cut = (cut_events.Trijet.masym < 0.15) & (cut_events.Trijet.mds < 0.175) & (cut_events.Trijet.delta > 125)
        # dask_hist_mass.fill(ak.flatten(cut_events.Trijet[cut].mass), "DeltaGr125QCD",weight=(x_sections[key] / (ak.num(qcd_events[key], axis=0)))
        # cut = (cut_events.Trijet.masym < 0.15) & (cut_events.Trijet.mds < 0.175) & (cut_events.Trijet.delta > 250)
        # dask_hist_mass.fill(ak.flatten(cut_events.Trijet[cut].mass), "DeltaGr250QCD",weight=(x_sections[key] / (ak.num(qcd_events[key], axis=0)))
        # cut_events = good_qcd_events[key] #[overallcut]
        # cut = ak.argmin(cut_events.Trijet.masym,axis=1,keepdims=True)
        # dask_hist_mass.fill(ak.flatten(cut_events.Trijet[cut].m), "MinAsyQCD",weight=(x_sections[key] / (ak.num(qcd_events[key], axis=0).compute())))
        print("Done with " + key)

dask_hist_mass.compute().plot1d()
plt.yscale('log')

plt.savefig('Run3/qcd_invmass.png')

# h4[:,"Full"].plot(stack=False, histtype="step")
# plt.legend()

# plt.savefig('Run3/invmass_full.png')
# plt.clf()

print("Done!")

client.close()



