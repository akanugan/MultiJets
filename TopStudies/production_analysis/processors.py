"""Custom processors, implementing coffea.processor.ProcessorABC.

Implements a couple of different processors that can then be run by an analyzer.
"""

import awkward as ak
import hist.dask as hda
from coffea.processor import ProcessorABC
from helper_functions import format_trijet_events


class SemiLeptonicTopTruthProcessor(ProcessorABC):
    """Processor that uses truth matching for SemiLeptonicTops.

    This uses the GenPart collection to find the correct ScoutingJet objects, to study
    the perfect world mass resolution of the ScoutingJet collection. It uses truth to
    find the leptonic top, then selects the jets from the hadronic tops and makes a
    histogram of the W and the top mass.
    """

    def __init__(self) -> None:
        """Init class."""

    def process(self, events) -> dict:
        dataset = events.metadata["dataset"]


        h_mass = (
            hda.Hist.new
            .StrCat(["w", "top"], name="object")
            .Log(1000, 30, 500., name="mass", label="Invariant Mass [GeV]")
            .Weight()
        )

        """
            What I'm trying to do here is find all of the W's and all of the b's from
            the hadronic top. The tricky part is sometimes, there is not a B or not a
            W. This causes a problem, since we need the arrays of W jets and b jets to
            be the same length when we take the invariant mass of the top. So we need
            to find all ofthe relevant objects, and cut the events that are missing one
            or the other.

            After those cuts, we need to then remake the arrays properly and we can be
            sure to expect the later arrays to be the same length.
        """
        truth = events.GenPart[
            (abs(events.GenPart.pdgId) == 24)
              & ( events.GenPart.hasFlags(["isLastCopy","isPrompt"]))
              ]

        w_to_jets_cut =(
            (abs(truth.distinctChildren[:,:,0].pdgId) == 1)
            | (abs(truth.distinctChildren[:,:,0].pdgId) == 2)
            | (abs(truth.distinctChildren[:,:,0].pdgId) == 3)
            | (abs(truth.distinctChildren[:,:,0].pdgId) == 4)
            )

        w_truth = truth[w_to_jets_cut]


        good_events = events[(ak.num(w_truth, axis=1) > 0)]

        w_truth = w_truth[ak.num(w_truth, axis=1) > 0]
        w_truth = w_truth[:,0]

        truth_b = good_events.GenPart[
            (abs(good_events.GenPart.pdgId) == 5)
            & ( good_events.GenPart.hasFlags(["isLastCopy"]))
            & (good_events.GenPart.distinctParentIdxG == w_truth.distinctParentIdxG)
            ]

        good_events = good_events[
            (ak.num(truth_b, axis=1) > 0)
            & (ak.num(w_truth.distinctChildren, axis=1) > 1)
            ]

        """
            Now we've cut out all events that are missing W's, b's, or the children of
            W's, so we can add the arrays later.
        """

        truth = good_events.GenPart[(abs(good_events.GenPart.pdgId) == 24) & ( good_events.GenPart.hasFlags(["isLastCopy","isPrompt"]))]

        w_to_jets_cut = (abs(truth.distinctChildren[:,:,0].pdgId) == 1) | (abs(truth.distinctChildren[:,:,0].pdgId) == 2) | (abs(truth.distinctChildren[:,:,0].pdgId) == 3) | (abs(truth.distinctChildren[:,:,0].pdgId) == 4)
        w_truth = truth[w_to_jets_cut]
        w_truth = w_truth[ak.num(w_truth, axis=1) > 0]
        w_truth = w_truth[:,0]
        w_jets_truth = w_truth.distinctChildren
        w_jets_truth = w_jets_truth[ak.num(w_jets_truth, axis=1) > 1]

        truth_b = good_events.GenPart[
            (abs(good_events.GenPart.pdgId) == 5)
            & ( good_events.GenPart.hasFlags(["isLastCopy"]) )
            & (good_events.GenPart.distinctParentIdxG == w_truth.distinctParentIdxG)
            ]

        truth_b = truth_b[:,0]
        first_jet = w_jets_truth[:,0]
        second_jet = w_jets_truth[:,1]

        """
            Now we've got all of our truth particles. Time to use matching to find
            candidates for these in the ScoutingJet.

            For now, I'm just going to find the nearest object using delta_r. I can't
            seem to make the "nearest" method work, so I instead found the index of
            the closest object and used the "ak.local_index" to match it.
        """


        candidate_one = good_events.ScoutingJet[
            ak.local_index(good_events.ScoutingJet,axis=1)
            == ak.argmin(first_jet.delta_r(good_events.ScoutingJet),axis=1)
            ]

        candidate_two = good_events.ScoutingJet[
            ak.local_index(good_events.ScoutingJet,axis=1)
            == ak.argmin(second_jet.delta_r(good_events.ScoutingJet),axis=1)
            ]

        w_candidate = candidate_one + candidate_two

        candidate_b = good_events.ScoutingJet[
            ak.local_index(good_events.ScoutingJet,axis=1)
            == ak.argmin(truth_b.delta_r(good_events.ScoutingJet),axis=1)
            ]

        top_candidate = w_candidate + candidate_b

        w_candidate = w_candidate[:,0]
        w_candidate = ak.drop_none(w_candidate,axis=0)
        top_candidate = top_candidate[:,0]
        top_candidate = ak.drop_none(top_candidate,axis=0)

        h_mass.fill(object="w", mass=w_candidate.mass)
        h_mass.fill(object="top", mass=top_candidate.mass)

        return {
            dataset: {
                "mass": h_mass,
            },
        }

    def postprocess(self, accumulator):
        pass

class SemiLeptonicTopCutProcessor(ProcessorABC):
    """Processor to find SemiLeptonicTops using cuts.

    This is intended to study the resolution of the ScoutingJet collection. The strategy
    is to look for leptonically decaying tops by identifying single leptons and MET, and
    then once ttbar is identified we can look at the hadronically decaying tops.
    """

    def __init__(self) -> None:
        """Init class."""

    def process(self, events) -> dict:
        dataset = events.metadata["dataset"]

        h_mass = (
            hda.Hist.new
            .StrCat(["w", "top"], name="object")
            .Log(1000, 30, 500., name="mass", label="Invariant Mass [GeV]")
            .Weight()
        )

        cut = (ak.num(events.ScoutingJet) >= 4)\
                & (events.ScoutingMET.pt > 40)\
                & (ak.sum(events.ScoutingJet.particleNet_prob_b == 0 ,axis=1) > 1)\
                & (ak.sum(events.ScoutingJet.particleNet_prob_b > 0.00001, axis=1) > 1)

        w_jet_cut = events[cut].ScoutingJet.particleNet_prob_b == 0
        b_jet_cut = events[cut].ScoutingJet.particleNet_prob_b > 0.00001

        non_b_jets = events[cut].ScoutingJet[w_jet_cut]
        b_jets = events[cut].ScoutingJet[b_jet_cut]
        w_candidate = non_b_jets[:,0] + non_b_jets[:,1]
        top_candidate = b_jets[:,0] + w_candidate

        h_mass.fill(object="w", mass=w_candidate.mass)
        h_mass.fill(object="top", mass=top_candidate.mass)

        return {
            dataset: {
                "mass": h_mass,
            },
        }

    def postprocess(self, accumulator):
        pass

class TrijetProcessor(ProcessorABC):
    """Processor to search for Trijets."""

    def __init__(self):
        """Init class."""

    def process(self, events):
        dataset = events.metadata["dataset"]

        good_events = format_trijet_events(events, jet_eta_cut=2.4)

        h_mass = (
            hda.Hist.new
            .StrCat(["Full","CutNoDelta","DeltaGr250","DeltaGr0","DeltaGr125","MinAsy"], growth=True, name="cuts")
            .Reg(1000, 100, 300, name="mass", label="Trijet Invariant Mass")
            .Weight()
        )

        h_HT = (
            hda.Hist.new
            .StrCat(["Full","CutNoDelta","DeltaGr250","DeltaGr0","DeltaGr125","MinAsy"], growth=True, name="cuts")
            .Reg(1000, 0, 3000, name="ht", label="Scalar Sum of Hadronic Transverse Energy")
            .Weight()
        )

        h_delta = (
            hda.Hist.new
            .StrCat(["Full","CutNoDelta","DeltaGr250","DeltaGr0","DeltaGr125","MinAsy"], growth=True, name="cuts")
            .Reg(1000, -1500, 1500, name="delta", label="Trijet Delta")
            .Weight()
        )

        h_lead_pt = (
            hda.Hist.new
            .StrCat(["Full","CutNoDelta","DeltaGr250","DeltaGr0","DeltaGr125","MinAsy"], growth=True, name="cuts")
            .Reg(1000, 0, 3000, name="pt", label="Leading Jet Pt")
            .Weight()
        )

        h_mass.fill(mass=ak.flatten(good_events.Trijet.mass), cuts="Full")
        h_HT.fill(ht=good_events.HT, cuts="Full")
        h_delta.fill(delta=ak.flatten(good_events.Trijet.delta,axis=1), cuts="Full")
        h_lead_pt.fill(pt=good_events.ScoutingJet[:,0].pt, cuts="Full")

        overallcut = (good_events.HT > 550) & (good_events.mds6332 < 1.25)
        cut_events = good_events[overallcut]

        cut = (cut_events.Trijet.masym < 0.15) & (cut_events.Trijet.mds < 0.175)
        h_mass.fill(mass=ak.flatten(cut_events.Trijet[cut].mass), cuts="CutNoDelta")
        h_HT.fill(ht=cut_events.HT, cuts="CutNoDelta")
        h_delta.fill(delta=ak.flatten(cut_events.Trijet[cut].delta,axis=1), cuts="CutNoDelta")
        h_lead_pt.fill(pt=cut_events.ScoutingJet[:,0].pt, cuts="CutNoDelta")

        cut = (cut_events.Trijet.masym < 0.15) & (cut_events.Trijet.mds < 0.175) & (cut_events.Trijet.delta > 0)
        h_mass.fill(mass=ak.flatten(cut_events.Trijet[cut].mass), cuts="DeltaGr0")
        h_HT.fill(ht=cut_events.HT, cuts="DeltaGr0")
        h_delta.fill(delta=ak.flatten(cut_events.Trijet[cut].delta,axis=1), cuts="DeltaGr0")
        h_lead_pt.fill(pt=cut_events.ScoutingJet[:,0].pt, cuts="DeltaGr0")

        cut = (cut_events.Trijet.masym < 0.15) & (cut_events.Trijet.mds < 0.175) & (cut_events.Trijet.delta > 125)
        h_mass.fill(mass=ak.flatten(cut_events.Trijet[cut].mass), cuts="DeltaGr125")
        h_HT.fill(ht=cut_events.HT, cuts="DeltaGr125")
        h_delta.fill(delta=ak.flatten(cut_events.Trijet[cut].delta,axis=1), cuts="DeltaGr125")
        h_lead_pt.fill(pt=cut_events.ScoutingJet[:,0].pt, cuts="DeltaGr125")

        cut = (cut_events.Trijet.masym < 0.15) & (cut_events.Trijet.mds < 0.175) & (cut_events.Trijet.delta > 250)
        h_mass.fill(mass=ak.flatten(cut_events.Trijet[cut].mass), cuts="DeltaGr250")
        h_HT.fill(ht=cut_events.HT, cuts="DeltaGr250")
        h_delta.fill(delta=ak.flatten(cut_events.Trijet[cut].delta,axis=1), cuts="DeltaGr250")
        h_lead_pt.fill(pt=cut_events.ScoutingJet[:,0].pt, cuts="DeltaGr250")

        cut_events = good_events #[overallcut]
        cut = ak.argmin(cut_events.Trijet.masym,axis=1,keepdims=True)
        h_mass.fill(mass=ak.flatten(cut_events.Trijet[cut].mass), cuts="MinAsy")
        h_HT.fill(ht=cut_events.HT, cuts="MinAsy")
        h_delta.fill(delta=ak.flatten(cut_events.Trijet[cut].delta,axis=1), cuts="MinAsy")
        h_lead_pt.fill(pt=cut_events.ScoutingJet[:,0].pt, cuts="MinAsy")

        return {
            dataset: {
                "mass": h_mass,
                "num_events": ak.num(events, axis=0),
                "HT": h_HT,
                "delta": h_delta,
                "lead_pt": h_lead_pt,
            },
        }


    def postprocess(self, accumulator):
        pass


class TrijetWriterProcessor(ProcessorABC):
    """Processor to search for Trijets."""

    def __init__(self):
        """Init class."""

    def process(self, events):
        dataset = events.metadata["dataset"]

        good_events = format_trijet_events(events, jet_eta_cut=2.4)

        return {
            dataset: {
                "Trijet": good_events.Trijet,
                "HT": good_events.HT,
                "mds6332": good_events.mds6332,
                "num_events": ak.num(events, axis=0),
            },
        }


    def postprocess(self, accumulator):
        pass
