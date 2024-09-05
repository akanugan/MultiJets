import awkward as ak

from coffea import processor
# from coffea.nanoevents.methods import candidate
# from coffea.dataset_tools import (
#     apply_to_fileset,
#     max_chunks,
#     preprocess,
# )

import hist.dask as hda

class SemiLeptonicTopProcessor(processor.ProcessorABC):
    def __init__(self):
        pass

    def process(self, events):
        dataset = events.metadata['dataset']


        # h_mass = (
        #     hda.Hist.new
        #     .StrCat(["w", "top"], name="object")
        #     .Log(1000, 30, 500., name="mass", label="Invariant Mass [GeV]")
        #     .Int64()
        # )

        # cut = (ak.num(events.ScoutingJet) >= 4)\
        #         & (events.ScoutingMET.pt > 40)\
        #         & (ak.sum(events.ScoutingJet.particleNet_prob_b == 0 ,axis=1) > 1)\
        #         & (ak.sum(events.ScoutingJet.particleNet_prob_b > 0.00001, axis=1) > 1)
        

        # w_jet_cut = events[cut].ScoutingJet.particleNet_prob_b == 0 
        # b_jet_cut = events[cut].ScoutingJet.particleNet_prob_b > 0.00001

        # non_b_jets = events[cut].ScoutingJet[w_jet_cut]
        # b_jets = events[cut].ScoutingJet[b_jet_cut]
        # w_candidate = non_b_jets[:,0] + non_b_jets[:,1]
        # top_candidate = b_jets[:,0] + w_candidate


        # truth = events.GenPart[(abs(events.GenPart.pdgId) == 24) & ( events.GenPart.hasFlags(['isLastCopy','isPrompt']))]

        # w_to_jets_cut = (abs(truth.children[:,:,0].pdgId) == 1) | (abs(truth.children[:,:,0].pdgId) == 2) | (abs(truth.children[:,:,0].pdgId) == 3) | (abs(truth.children[:,:,0].pdgId) == 4)

        # w_truth = truth[w_to_jets_cut]
        # w_truth = w_truth[ak.num(w_truth, axis=1) > 0]
        # w_truth = w_truth[:,0]
        # w_jets_truth = w_truth.children
        # w_jets_truth = w_jets_truth[ak.num(w_jets_truth, axis=1) > 1]

        # first_jet = w_jets_truth[:,0]
        # second_jet = w_jets_truth[:,1]

        # # first_jet.nearest(events.ScoutingJet).compute()


        # candidate_one = events.ScoutingJet[ak.local_index(events.ScoutingJet,axis=1) == ak.argmin(first_jet.delta_r(events.ScoutingJet),axis=1)]
        # candidate_two = events.ScoutingJet[ak.local_index(events.ScoutingJet,axis=1) == ak.argmin(second_jet.delta_r(events.ScoutingJet),axis=1)]

        # w_candidate = candidate_one + candidate_two

        # truth_b = events.GenPart[(abs(events.GenPart.pdgId) == 5) & ( events.GenPart.hasFlags(['isLastCopy'])) & (events.GenPart.distinctParentIdxG == w_truth.distinctParentIdxG)]
        # truth_b = truth_b[ak.num(truth_b, axis=1) >0]
        # truth_b = truth_b[:,0]
        # candidate_b = events.ScoutingJet[ak.local_index(events.ScoutingJet,axis=1) == ak.argmin(truth_b.delta_r(events.ScoutingJet),axis=1)]
        
        # top_candidate = w_candidate + candidate_b

        # h_mass.fill(object="w", mass=ak.flatten(events.ScoutingJet.pt))
        # h_mass.fill(object="top", mass=ak.flatten(events.ScoutingJet.pt))

        return {
            dataset: {
                "entries": ak.num(events, axis=0),
                # "mass": h_mass,
            }
        }

    def postprocess(self, accumulator):
        pass