"""Analyzer for the semi-leptonic tops.

Runs the processor over the selected samples, and plots the histograms.
"""

import sys

import dask
import hist.dask as hda
import matplotlib.pyplot as plt
import uproot
from coffea.dataset_tools import (
    apply_to_fileset,
    max_chunks,
    preprocess,
)
from coffea.nanoevents import NanoEventsFactory, ScoutingNanoAODSchema
from distributed import Client
from lpcjobqueue import LPCCondorCluster

from processors import SemiLeptonicTopTruthProcessor


def run_analysis(client):
    file_list = [line.strip("\n") for line in open("filelists/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8_0000.txt")] + [line.strip('\n') for line in open("filelists/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8_0001.txt").readlines()] + [line.strip('\n') for line in open("filelists/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8_0002.txt").readlines()]
    file_list = ["root://cmseos.fnal.gov//" + string for string in file_list]

    ScoutingNanoAODSchema.warn_missing_crossrefs = False

    # small_events = NanoEventsFactory.from_root(
    #     {file : "Events" for file in file_list[0:10]},
    #     schemaclass=ScoutingNanoAODSchema,
    #     metadata={"dataset": "HadronicTops"},
    # ).events()
    # p = SemiLeptonicTopProcessor()

    # out = p.process(small_events)

    # print("starting computation")

    # (computed,) = dask.compute(out)

    fileset = {
        "SemiLeptonicTop": {
            "files": {file : "Events" for file in file_list[0:10]},
        },
    }


    dataset_runnable, dataset_updated = preprocess(
        fileset,
        align_clusters=False,
        step_size=100_000,
        files_per_batch=1,
        skip_bad_files=True,
        save_form=False,
    )

    print("to_compute")

    to_compute = apply_to_fileset(
                SemiLeptonicTopTruthProcessor(),
                dataset_runnable,
                schemaclass=ScoutingNanoAODSchema,
                )

    print("compute")

    (out,) = dask.compute(to_compute)

    print(out)


    return out


def plot_mass_histograms(mass_hist, file, name: str):
    file["mass"] = mass_hist

    fig, ax = plt.subplots()
    mass_hist["mass"].plot1d(ax=ax)

    ax.set_yscale("log")
    ax.legend()

    plt.savefig("plots/" + name + ".png")

    fig, ax = plt.subplots()
    mass_hist["mass"].plot1d(ax=ax)
    ax.set_yscale("linear")
    ax.legend()

    plt.savefig("plots/" + name + "_lin.png")


if __name__ == "__main__":
    cluster = LPCCondorCluster(memory="8GB")
    cluster.adapt(minimum=0, maximum=30)

    with Client(cluster) as client:
        result = run_analysis(client)

    if len(sys.argv) > 1:
        file = uproot.recreate(str(sys.argv[1]) + ".root")
        plot_mass_histograms(result["SemiLeptonicTop"]["SemiLeptonicTop"],file,str(sys.argv[1]))
    else:
        file = uproot.recreate("default.root")
        plot_mass_histograms(result["SemiLeptonicTop"]["SemiLeptonicTop"],file,"default")
