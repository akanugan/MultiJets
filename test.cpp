void test(){


    std::vector<std::string> file_names;
    std::string path = "slimmed_ntuples/slimmedNtup_slimmed_ntuple_QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8.root";
    

    TFile *f =  TFile::Open(path.c_str(), "read");
    TTree *t = f->Get<TTree>("events");

    Float_t jtrip_mass[20];


    t->SetBranchAddress("jtrip_mass",&jtrip_mass);


    const Int_t nentries = (Int_t)t->GetEntries();
    std::cout << "Events in sample:" << nentries << std::endl;

    for (int i=0; i < nentries; i++){
        t->GetEntry(i);
        std::cout << "jtrip_mass " << i << ": " << jtrip_mass[4] << std::endl;

    }
    std::cout << "here2" << std::endl;
}