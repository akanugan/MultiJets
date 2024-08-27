import awkward as ak

from coffea import processor
from coffea.nanoevents.methods import candidate
from coffea.dataset_tools import (
    apply_to_fileset,
    max_chunks,
    preprocess,
)

import hist.dask as hda

from distributed import Client

class SemiLeptonicTopProcessor(processor.ProcessorABC):
    def __init__(self):
        pass

    def process(self, events):
        dataset = events.metadata['dataset']


        h_mass = (
            hda.Hist.new
            .StrCat(["opposite", "same"], name="sign")
            .Log(1000, 0.2, 200., name="mass", label="$m_{\mu\mu}$ [GeV]")
            .Int64()
        )

        cut = (ak.num(events.ScoutingMuon) == 2) & (ak.sum(events.ScoutingMuon.charge, axis=1) == 0)
        # add first and second muon in every event together
        dimuon = events.ScoutingMuon[cut][:, 0] + events.ScoutingMuon[cut][:, 1]
        h_mass.fill(sign="opposite", mass=dimuon.mass)

        cut = (ak.num(events.ScoutingMuon) == 2) & (ak.sum(events.ScoutingMuon.charge, axis=1) != 0)
        dimuon = events.ScoutingMuon[cut][:, 0] + events.ScoutingMuon[cut][:, 1]
        h_mass.fill(sign="same", mass=dimuon.mass)


        return {
            dataset: {
                "entries": ak.num(events, axis=0),
                "mass": h_mass,
            }
        }

    def postprocess(self, accumulator):
        pass

