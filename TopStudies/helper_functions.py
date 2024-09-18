"""Various physics functions used in the processors."""

import awkward as ak
from coffea.analysis_tools import PackedSelection

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

def temp():
    sel = PackedSelection()

def format_trijet_events(ev, jet_eta_cut: float=2.4):
    # vec.register_awkward()

    # sel = PackedSelection()
    # sel.add("SixJets", ak.num(ev.ScoutingJet[ev.ScoutingJet.eta < jet_eta_cut], axis=1) >= 6)

    # result = ev[sel.all("SixJets")]

    # result = ev[ak.num(ev.ScoutingJet[ev.ScoutingJet.eta < 2.4], axis=1) >= 6]
    result = ev
    # selected_jets = result.ScoutingJet[result.ScoutingJet.eta < jet_eta_cut][:,0:6]
    # trijet = ak.combinations(selected_jets, 3, fields=["j1","j2","j3"])

    # mds_val, m12, m13, m23 = tri_mds(trijet)

    # result["Trijet"] = ak.zip(
    #     {
    #         "j1": trijet.j1,
    #         "j2": trijet.j2,
    #         "j3": trijet.j3,
    #         "px": trijet.j1.px + trijet.j2.px + trijet.j3.px,
    #         "py": trijet.j1.py + trijet.j2.py + trijet.j3.py,
    #         "pz": trijet.j1.pz + trijet.j2.pz + trijet.j3.pz,
    #         "e": trijet.j1.E + trijet.j2.E + trijet.j3.E,
    #         "masym": mass_asymmetry(selected_jets,trijet),
    #         "mds": mds_val,
    #         "m12": m12,
    #         "m13": m13,
    #         "m23": m23,
    #         "delta": tri_delta(trijet),
    #         "mds63": tri_mds63(selected_jets, trijet),
    #     },
    #     with_name="Momentum4D",
    # )

    # result["HT"] = ak.sum(abs(result.ScoutingJet.pt), axis=1)
    # result["mds6332"] = tri_mds6332(selected_jets, trijet, mds_val)

    return result
