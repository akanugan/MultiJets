#!/bin/sh

executable=$1
filelist=$2
isdata=$3

currDir=$(pwd)

# Set up the CMSSW environment or any other necessary setup
source /cvmfs/cms.cern.ch/cmsset_default.sh

export PATH=$USER_PATH:$PATH
export PATH=$PATH:/opt/conda/bin
export PATH=$PATH:/usr/local/bin/condor_submit
export PYTHONWARNINGS="ignore"
echo "PATH"
$PATH

#export SCRAM_ARCH=slc7_amd64_gcc820
export HOME=.

scram project CMSSW_10_3_1
cd CMSSW_10_3_1/src/
eval `scramv1 runtime -sh`
pwd
echo "ls"
pwd
cd -

echo "hostname"
hostname

python $1 $2 $3 