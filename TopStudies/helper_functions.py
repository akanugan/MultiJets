"""Various physics functions used in the processors."""

import awkward as ak
from coffea.lookup_tools import extractor

# from coffea.analysis_tools import PackedSelection

x_sections = {
                "QCD_PT-120to170": 445800.0,
                "QCD_PT-170to300": 113700.0,
                "QCD_PT-300to470": 7589.0,
                "QCD_PT-470to600": 626.4,
                "QCD_PT-600to800": 178.6,
                "QCD_PT-800to1000": 30.57,
                "QCD_PT-1000to1400": 8.92,
                "QCD_PT-1400to1800": 0.8103,
                "QCD_PT-1800to2400": 0.1148,
                "QCD_PT-2400to3200": 0.007542,
                "QCD_PT-3200": 0.0002331,
                "TTto4Q": 762.1,
}

def get_QCD_keys():
    return [key for key in x_sections if "QCD" in key]

def x_sec(name: str) -> float:
    key = sample_name(name)
    if key == None:
        return 0.0
    return x_sections[key]

def sample_name(name: str) -> str:
    """Find a sample key in a given string.

    Parameters
    ----------
    name : string
        The name of a file you want parsed for a sample key

    Returns
    -------
    string
        The first sample key found in the string. Returns None if no sample key is
        found.

    """
    for key in x_sections:
        if key in name:
            return key
    return None

def mass_asymmetry(sj, tj):
    total_p4 = sj[:,0] + sj[:,1] + sj[:,2] + sj[:,3] + sj[:,4] + sj[:,5]
    cart = ak.cartesian([total_p4, tj])
    vector = (cart["1"].j1 + cart["1"].j2 + cart["1"].j3)
    other_vector = (cart["0"] - vector)

    vm = vector.mass
    ovm =other_vector.mass
    masym = (vm - ovm)/(vm + ovm)
    return masym

def d_phi(sj, tj):
    total_p4 = sj[:,0] + sj[:,1] + sj[:,2] + sj[:,3] + sj[:,4] + sj[:,5]
    cart = ak.cartesian([total_p4, tj])
    vector = (cart["1"].j1 + cart["1"].j2 + cart["1"].j3)
    other_vector = (cart["0"] - vector)

    vp = vector.phi
    ovp = other_vector.phi

    return vp - ovp

def tri_mds(tj) -> tuple:
    """Find the mds scores and pairs of invariant masses.

    One problem is I haven't found a good way to sort the m12,m13,m23 pairs in a lazy,
    Dask way. When that becomes important I'll work on it.
    """
    den=((tj.j1+tj.j2+tj.j3).mass**2)+(tj.j1.mass**2)+(tj.j2.mass**2)+(tj.j3.mass**2)

    #it would be nice if these were sorted, but
    #struggling to do it with coffea
    m12=((tj.j1+tj.j2).mass**2)/den
    m13=((tj.j1+tj.j3).mass**2)/den
    m23=((tj.j2+tj.j3).mass**2)/den


    r13 = 1/(3**0.5)
    mds=((m12**0.5)-r13)**2 + ((m13**0.5)-r13)**2 + ((m23**0.5)-r13)**2

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

def apply_JEC_MC(ev, dir_name, name, type):
    ext = extractor()
    ext.add_weight_sets(
        [
            "* * corrections/" + dir_name + "/" + name + "_L1FastJet_AK4PF" + type + ".txt",
            "* * corrections/" + dir_name + "/" + name + "_L2Residual_AK4PF" + type + ".txt",
            "* * corrections/" + dir_name + "/" + name + "_L2Relative_AK4PF" + type + ".txt",
            "* * corrections/" + dir_name + "/" + name + "_L3Absolute_AK4PF" + type + ".txt",
            "* * corrections/" + dir_name + "/" + name + "_L2L3Residual_AK4PF" + type + ".txt",
            #"* * corrections/Summer22EE_22Sep2023_V2_MC/Summer22EE_22Sep2023_V2_MC_Uncertainty_AK4PFPuppi.junc.txt",
        ],
    )
    ext.finalize()


    jec_stack_names = [
        name + "_L1FastJet_AK4PF"+ type,
        name + "_L2Relative_AK4PF"+ type,
        # name + "_L2Residual_AK4PF"+ type,
        name + "_L3Absolute_AK4PF"+ type,
        # name + "_L2L3Residual_AK4PF"+ type,
        #"Summer22EE_22Sep2023_V2_MC_Uncertainty_AK4PFPuppi",
    ]

    evaluator = ext.make_evaluator()

    corr_jets = ev.ScoutingJet
    corr_jets["pt_raw"] = corr_jets.pt

    for i in range(len(jec_stack_names)):
        scale_factor = evaluator[jec_stack_names[i]](corr_jets.eta, corr_jets.pt, ev.ScoutingRho, corr_jets.area)
        corr_jets["pt"] = scale_factor*corr_jets.pt
    return corr_jets

def tight_jets(ev,jet_eta_cut: float=2.4, jet_pt_cut: float=30):
# changed this to tight_jet or something like that
# clean jet or jet cleaning
    res = ev
    res["ScoutingJet"] = apply_JEC_MC(ev, "Summer22EE_22Sep2023_V2_MC", "Summer22EE_22Sep2023_V2_MC","Puppi")
    jet_cut = (abs(res.ScoutingJet.eta) < jet_eta_cut) \
          & (res.ScoutingJet.pt > jet_pt_cut) \
          & (res.ScoutingJet.neHEF < 0.90) \
          & (res.ScoutingJet.neEmEF < 0.90) \
          & (res.ScoutingJet.nConstituents > 1) \
          & (res.ScoutingJet.muEmEF < 0.80) \
          & (res.ScoutingJet.chHEF > 0.01) \
          & (res.ScoutingJet.nCh > 0) \
          & (res.ScoutingJet.chEmEF < 0.80)
    res["ScoutingJet"] = res.ScoutingJet[jet_cut]
    return res

def format_trijet_events(ev, jet_eta_cut: float=2.4, jet_pt_cut: float=30):

    # sel = PackedSelection()
    # sel.add("SixJets", ak.num(ev.ScoutingJet[ev.ScoutingJet.eta < jet_eta_cut], axis=1) >= 6)

    tight = tight_jets(ev,jet_eta_cut,jet_pt_cut)

    result = tight[ak.num(tight.ScoutingJet,axis=1) >= 6]

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
            "dphi": d_phi(selected_jets,trijet),
            "delta": tri_delta(trijet),
            "mds63": tri_mds63(selected_jets, trijet),
        },
        with_name="Momentum4D",
    )

    result["HT"] = ak.sum(abs(result.ScoutingJet.pt), axis=1)
    result["mds6332"] = tri_mds6332(selected_jets, trijet, mds_val)

    return result
