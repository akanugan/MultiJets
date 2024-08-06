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

cluster = LPCCondorCluster(memory="4GB", disk="10GB")
cluster.adapt(minimum=0, maximum=800)
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

small_events = NanoEventsFactory.from_root(
    {file : "Events" for file in file_list},
    schemaclass=ScoutingNanoAODSchema,
    metadata={"dataset": "TTto4Q_TuneCP5_13p6TeV_powheg-pythia8"},
).events()

qcd_events = {}

for f in [line.strip('\n') for line in open("qcd_files.txt").readlines()]:
    file_list = [line.strip('\n') for line in open(f).readlines()]
    file_list = ["root://cmseos.fnal.gov//" + string for string in file_list]
    qcd_events[sample_name(f)] = NanoEventsFactory.from_root(
        {file : "Events" for file in file_list},
        schemaclass=ScoutingNanoAODSchema,
        metadata={"dataset": sample_name(f)},
        ).events()
    
    #num_events = ak.num(qcd_events[sample_name(f)],axis=0).compute()
    #qcd_events[sample_name(f)]["Weight"] = dak.Array(np.full(num_events,(x_sections[sample_name(f)] / num_events)))

weights = {}

for ky in x_sections.keys():
    if ky not in ['TTto4Q']:
        weights[ky] = (x_sections[ky] / (ak.num(qcd_events[ky], axis=0)).compute())
    else:
        weights[ky] = (x_sections[ky] / (ak.num(small_events, axis=0)).compute())

vec.register_awkward()

def format_good_events(ev):
    sel = PackedSelection()
    sel.add("SixJets", ak.num(ev.ScoutingJet[ev.ScoutingJet.eta < 2.4], axis=1) >5)

    result = ev[sel.all("SixJets")]
    selected_jets = result.ScoutingJet[result.ScoutingJet.eta < 2.4][:,0:6]
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

print("Made it to histogramming!")

def fill_cut_hist(tmp_hist, ev, cat, label):
    overallcut = (ev.HT > 550)
    cut_events = ev[overallcut]
    cut = (cut_events.Trijet.masym < 0.15) & (cut_events.Trijet.mds < 0.175) & (cut_events.Trijet.delta > 250)
    tmp_hist.fill(ak.flatten(cut_events.Trijet[cut].m), cat, weight=weights[label])

dask_hist_mass =  (
    hda.Hist.new.Reg(60, 100, 300, name="mass_qcd", label="Inv Mass [GeV]")
    .StrCat(["Full","Cut","FullTT","CutTT"], name='dataset')
    .Weight()
)

for ky in x_sections.keys():
    if ky not in ['TTto4Q']:
        dask_hist_mass.fill(ak.flatten(good_qcd_events[ky].Trijet.m), "Full", weight=weights[ky])
        fill_cut_hist(dask_hist_mass, good_qcd_events[ky], "Cut", ky)

dask_hist_mass.fill(ak.flatten(good_events.Trijet.m), "FullTT", weight=weights['TTto4Q'])
fill_cut_hist(dask_hist_mass, good_events, 'CutTT', 'TTto4Q')

hm = dask_hist_mass.compute()

hm[:,'Full'].plot1d(stack=True,label="QCD")
hm[:,'FullTT'].plot1d(stack=True,label="TTbar")

plt.yscale('log')
plt.legend()
plt.savefig("Run3/invmass_qcd_full.png")

plt.clf()

hm[:,'Cut'].plot1d(stack=True,label="QCD")
hm[:,'CutTT'].plot1d(stack=True,label="TTbar")

plt.yscale('log')
plt.legend()
plt.savefig("Run3/invmass_qcd.png")

client.close()