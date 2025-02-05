"""Get filesets from here instead of doing them manually."""

from helper_functions import sample_name


def small_ttbar_fileset():
    file_list = [line.strip("\n") for line in open("filelists/TTto4Q_TuneCP5_13p6TeV_powheg-pythia8_0000.txt").readlines()] + [line.strip("\n") for line in open("filelists/TTto4Q_TuneCP5_13p6TeV_powheg-pythia8_0001.txt").readlines()]
    file_list = ["root://cmseos.fnal.gov//" + string for string in file_list]

    fileset = {
        "TTbar": {
            "files": {file : "Events" for file in file_list[0:40]},
        },
    }
    return fileset


def mc_fileset():
    file_list = [line.strip("\n") for line in open("filelists/TTto4Q_TuneCP5_13p6TeV_powheg-pythia8_0000.txt").readlines()] + [line.strip("\n") for line in open("filelists/TTto4Q_TuneCP5_13p6TeV_powheg-pythia8_0001.txt").readlines()]
    file_list = ["root://cmseos.fnal.gov//" + string for string in file_list]

    fileset = {
        "TTbar": {
            "files": {file : "Events" for file in file_list},
        },
    }

    for f in [line.strip("\n") for line in open("filelists/qcd_files.txt")]:
        file_list = [line.strip("\n") for line in open("filelists/" + f)]
        file_list = ["root://cmseos.fnal.gov//" + string for string in file_list]
        name = sample_name(f)
        fileset[name] = {
            "files": {file : "Events" for file in file_list},
        }

    return fileset

def data_test_fileset():
    file_list = [line.strip("\n") for line in open("filelists/2022_data/crab_ScoutingPFRun3_Run2022F_360335-360941_0002.txt")]
    file_list = ["root://cmseos.fnal.gov//" + string for string in file_list]

    return {
        "Run2022F_360335-360941_0002": {
             "files": {file : "Events" for file in file_list},
        },
    }
