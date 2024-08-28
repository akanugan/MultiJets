import awkward as ak

from coffea import processor
from coffea.nanoevents.methods import candidate
from coffea.dataset_tools import (
    apply_to_fileset,
    max_chunks,
    preprocess,
)

import hist.dask as hda

class SemiLeptonicTopProcessor(processor.ProcessorABC):
    def __init__(self):
        pass

    def process(self, events):
        dataset = events.metadata['dataset']


        h_mass = (
            hda.Hist.new
            .StrCat(["w", "top"], name="object")
            .Log(1000, 70, 500., name="mass", label="$m_{\mu\mu}$ [GeV]")
            .Int64()
        )

        cut = (ak.num(events.ScoutingJet) >= 4) & (events.ScoutingMET.pt > 40) & (ak.sum(events.ScoutingJet.particleNet_prob_b < 0.001 ,axis=1) > 1)
        w_jet_cut = events[cut].ScoutingJet.particleNet_prob_b < 0.001 
        b_jet_cut = events[cut].ScoutingJet.particleNet_prob_b > 0.1

        non_b_jets = events[cut].ScoutingJet[w_jet_cut]
        b_jets = events[cut].ScoutingJet[b_jet_cut]
        w_candidate = non_b_jets[:,0] + non_b_jets[:,1]
        top_candidate = b_jets[:,0] + w_candidate

        

        h_mass.fill(object="w", mass=w_candidate.mass)

        h_mass.fill(object="top", mass=top_candidate.mass)


        return {
            dataset: {
                "entries": ak.num(events, axis=0),
                "mass": h_mass,
            }
        }

    def postprocess(self, accumulator):
        pass