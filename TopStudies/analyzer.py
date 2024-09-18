"""Analyzer for the semi-leptonic tops.

Runs the processor over the selected samples, and plots the histograms.
"""

from time import sleep

import dask
import matplotlib.pyplot as plt
from coffea.dataset_tools import (
    apply_to_fileset,
    preprocess,
)
from coffea.nanoevents import NanoEventsFactory, ScoutingNanoAODSchema
from coffea.processor import ProcessorABC
from distributed import Client
from lpcjobqueue import LPCCondorCluster

from processors import TrijetProcessor


def run__preprocessed_analysis(processor: ProcessorABC, file_list: list):
    fileset = {
        "SemiLeptonicTop": {
            "files": {file : "Events" for file in file_list},
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
                processor(),
                dataset_runnable,
                schemaclass=ScoutingNanoAODSchema,
                )

    print("compute")

    (computed,) = dask.compute(to_compute)

    print(computed)


    return computed

def run_analysis(processor: ProcessorABC, file_list: list, metadata: str="Sample"):

    ScoutingNanoAODSchema.warn_missing_crossrefs = False

    print("entering ScoutingNanoAODSchema")

    small_events = NanoEventsFactory.from_root(
        {file : "Events" for file in file_list},
        schemaclass=ScoutingNanoAODSchema,
        metadata={"dataset": metadata},
    ).events()

    print("entering processor")

    p = processor()

    out = p.process(small_events)

    print("starting computation")

    (computed,) = dask.compute(out)

    return computed

def plot_mass_histograms(mass_hist, file, name: str) -> None:
    file["mass"] = mass_hist["mass"]
    # file["top_mass"] = mass_hist["mass"]

    fig, ax = plt.subplots()
    mass_hist["mass"].plot1d(ax=ax)

    ax.set_yscale("log")
    ax.legend()

    plt.savefig("plots/" + name + "_mass.png")

    fig, ax = plt.subplots()
    mass_hist["mass"].plot1d(ax=ax)
    ax.set_yscale("linear")
    ax.legend()

    plt.savefig("plots/" + name + "_mass_lin.png")

if __name__ == "__main__":
    cluster = LPCCondorCluster(memory="2GB")
    cluster.adapt(minimum=1, maximum=2)

    #file_list = [line.strip("\n") for line in open("filelists/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8_0000.txt")] + [line.strip("\n") for line in open("filelists/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8_0001.txt")] + [line.strip("\n") for line in open("filelists/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8_0002.txt")]
    file_list = [line.strip("\n") for line in open("filelists/TTto4Q_TuneCP5_13p6TeV_powheg-pythia8_0000.txt").readlines()] + [line.strip("\n") for line in open("filelists/TTto4Q_TuneCP5_13p6TeV_powheg-pythia8_0001.txt").readlines()]
    file_list = ["root://cmseos.fnal.gov//" + string for string in file_list]


    print("entering analyzer")
    with Client(cluster) as client:
        result = run_analysis(TrijetProcessor, file_list[5:20], metadata="Trijet")
        print()
        print()
        print()
        print(client.get_worker_logs())


    sleep(15)
    print(result)

    # if len(sys.argv) > 1:
    #     file = uproot.recreate(str(sys.argv[1]) + ".root")
    #     plot_mass_histograms(result["Trijet"],file,str(sys.argv[1]))
    # else:
    #     file = uproot.recreate("default.root")
    #     plot_mass_histograms(result["Trijet"],file,"default")
