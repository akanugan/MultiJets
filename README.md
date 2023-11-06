# MultiJets

Example Ntuplizer:
`python make_flat_jettuple_ak4.py Wjets.txt 0 6`

To run on condor:
`python condor_ntuplizer.py -i filelist/QCD_test.txt -n 1`

Analyzer:
`make`
`./AnaExe merged_ntuple_file.txt outFile.root MC`