void test(){


    std::vector<std::string> file_names;
    std::string path = "slimmed_ntuples/slimmedNtup_slimmed_ntuple_QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8.root";
    

    TFile *f = new TFile(path.c_str(), "read");
    TTree *t = f->Get<TTree>("events");

    //t->SetBranchStatus("*",0);

    Float_t jtrip_mass = 0;
    Float_t Event = 0;
        
    t->SetBranchAddress("jtrip_mass",&jtrip_mass);
    t->SetBranchStatus("jtrip_mass",1);
    t->SetBranchAddress("Event",&Event);
    t->SetBranchStatus("Event",1);


    const Int_t nentries = (Int_t)t->GetEntries();
    std::cout << "Events in sample:" << nentries << std::endl;

    for (int i=0; i < nentries; i++){

        auto output = t->GetEntry(i);
        
       //if (i %100 == 0){
            std::cout << "output: " << output << std::endl;
            //std::cout << "nentries: " << nentries << std::endl;
            std::cout << "jtrip_mass " << i << ": " << jtrip_mass << std::endl;
            std::cout << "Event " << i << ": " << Event << std::endl << std::endl;
        //}

        if (i > 1000){
            break;
        }
        std::cout << "here1" << std::endl;
    }
    delete t;
    f->Close();
    std::cout << "here2" << std::endl;
}