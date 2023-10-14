#!/bin/bash

mkdir -p condor_output
mkdir -p slimmed_ntuples

# Move files that meet the specified conditions to the condor_output directory
for file in FileList_* *.condor *.stderr *.stdout *.submit; do
    mv "$file" condor_output/
done

for file in slimmedNtup_*; do
    mv "$file" slimmed_ntuples/
done
