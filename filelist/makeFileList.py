import os

datasets = ['DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/',
'QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/',
'QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/',
'QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/',
'QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8/',
'QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8/',
'QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/',
'TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/',
'TTJets_TuneCP5_13TeV-madgraphMLM-pythia8/',
'WJetsToQQ_HT-800toInf_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8/',
'WJetsToQQ_HT400to600_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8/',
'WJetsToQQ_HT600to800_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8/',
'ZJetsToQQ_HT-800toInf_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8/',
'ZJetsToQQ_HT400to600_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8/',
'ZJetsToQQ_HT600to800_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8/',  
]

ntup_dir = '/eos/uscms/store/group/lpctrig/abhijith/mc_samples2017/'
file_extension = '.root'

for dataset in datasets:
    file_list = []
    start_directory = os.path.join(ntup_dir, dataset)

    for root, dirs, files in os.walk(start_directory):
        for file in files:
            if file.endswith(file_extension):
                file_path = os.path.join(root, file)
                file_list.append(file_path)

    output_file = '_'.join(dataset.split('_')[:2]) + '.txt'

    with open(output_file, 'w') as f:
        for file_path in file_list:
            f.write(file_path + '\n')

    print(f"Saving {dataset} as: {output_file}")
