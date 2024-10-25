"""Analyzer for the semi-leptonic tops.

Runs the processor over the selected samples, and plots the histograms.
"""

import sys

import dask
import matplotlib.pyplot as plt
import uproot
from coffea.dataset_tools import (
    apply_to_fileset,
    preprocess,
)
from coffea.nanoevents import NanoAODSchema, NanoEventsFactory
from coffea.processor import ProcessorABC
from distributed import Client
from lpcjobqueue import LPCCondorCluster

from filelists_helper import small_ttbar_fileset
from processors import TrijetWriterProcessor


class ScoutingNanoAODSchema(NanoAODSchema):

    mixins = {
        **NanoAODSchema.mixins,
        "ScoutingJet": "Jet",
    }


def run_preprocessed_analysis(
        processor: ProcessorABC,
        file_list: list,
        metadata:str="Sample"):


    dataset_runnable, dataset_updated = preprocess(
        file_list,
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

def plot_mass_histograms(mass_hist, name: str) -> None:
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
    tag = str(sys.argv[1]) if len(sys.argv) > 1 else "default"

    cluster = LPCCondorCluster(memory="3GB", log_directory="/uscmst1b_scratch/lpc1/3DayLifetime/jlawless/")
    cluster.adapt(minimum=1, maximum=200)

    fileset = small_ttbar_fileset()

    print("entering analyzer")
    with Client(cluster) as client:
        result = run_preprocessed_analysis(TrijetWriterProcessor, fileset, metadata="Trijet")

    print(result)

    file = uproot.recreate(str(sys.argv[1]) + ".root")
    for key in fileset:
        trij = result[key][key]["Trijet"]
        file["tree"] = {
            "trijet": {
                "px": trij.px,
                "py": trij.py,
                "pz": trij.pz,
                "e": trij.e,
                "masym": trij.masym,
                "mds": trij.mds,
                "m12": trij.m12,
                "m13": trij.m13,
                "m23": trij.m23,
                "dphi": trij.dphi,
                "delta": trij.delta,
                "mds63": trij.mds63,
            },
            "HT": result[key][key]["HT"],
            "mds6332": result[key][key]["mds6332"],
        }
        file["ev/" + key] = str(result[key][key]["num_events"])

    # file = uproot.recreate(str(sys.argv[1]) + ".root")
    # for key in fileset:
    #     file["mass/" + key] = result[key][key]["mass"]
    #     file["ev/" + key] = str(result[key][key]["num_events"])
    #     file["ht/" + key] = result[key][key]["HT"]
    #     file["delta/" + key] = result[key][key]["delta"]
    #     file["lead_pt/" + key] = result[key][key]["lead_pt"]

    #plot_mass_histograms(result["TTbar"]["TTbar"],tag)
