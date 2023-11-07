//made a class Sample to hold all a tree
//and all of the cross section related things at 
//the same time. On construction uses the x_section 
//map to automatically get the x_section for this sample.
//Relies on the fact that these are QCD samples with the 
//string "QCD_HT###to###_" somewhere present
class QCDSample {
    public:
        TTree *tree;
        TFile *file;
        std::string name;

        float pre_cut_events;
        float x_section;
        float weight;


        QCDSample(TTree *tr, TFile *fi, float we, std::string na, std::map<std::string,float> x_sections) {
                tree = tr;
                file = fi;
                pre_cut_events = we;
                

                auto start = na.find("QCD_HT");
                auto end = na.find("_", start + 5);
                std::string target = na.substr(start,end - start);
                name = na.substr(start);
                x_section = x_sections[target];
                weight = x_section / pre_cut_events;
        }
};

void analyzer(){
    //x-secs times filter eff in picobarns of QCD HT bins
    //need to get 300to500 bin x_sec at some point
    std::map<std::string,float> x_sections;
    x_sections["QCD_HT300to500"] = 0;
    x_sections["QCD_HT500to700"] = 29370;
    x_sections["QCD_HT700to1000"] = 6524;
    x_sections["QCD_HT1000to1500"] = 1064;
    x_sections["QCD_HT1500to2000"] =121.5;
    x_sections["QCD_HT2000toInf"] = 25.42;


    //Get all files in this directory
    //at some point can fix this to have different samples in different file lists
    std::vector<std::string> file_names;
    std::string path = "full_ntuples/";
    for (const auto & entry : std::filesystem::directory_iterator(path)){
            file_names.push_back(entry.path());
    }

    //Get trees and relevant x-section stuff for each tree
    std::vector<QCDSample> trees;
    //need to declare the iterator f outside of this class to ensure files stay in scope.
    TFile *f;
    TTree *t;
    QCDSample *q;
    for (auto i = file_names.begin(); i != file_names.end(); ++i){  
        f = new TFile(i->c_str(), "read");
        t = f->Get<TTree>("events");
        q = new QCDSample(t,f,f->Get<TH1>("cut_flow_hist")->GetBinContent(1),*i, x_sections);
        trees.push_back(*q);
        std::cout << trees.back().tree->GetEntries() << ", " << trees.back().pre_cut_events << ", " << trees.back().name << ", "<<trees.back().x_section <<std::endl;
    }

    TFile *output_hists = new TFile("analyzed_histograms.root","recreate");

    std::map<std::string,TH1*> histograms;
    histograms["mass_unweighted"] =  new TH1F("mass_unweighted", "Unweighted Invariant Mass of Triplets, JEC included", 70,0,2500);
    histograms["mass_weighted"] =  new TH1F("mass_weighted", "Weighted Invariant Mass of Triplets, JEC included", 70,0,2500);
    
    for (auto current_sample = trees.begin(); current_sample != trees.end(); ++current_sample){
        std::cout << "Processing sample: " << current_sample->name << std::endl;
        



        Float_t jtrip_mass[20];
        float Event = 0;
        
        current_sample->tree->SetBranchAddress("jtrip_mass",&jtrip_mass);
        // current_sample->tree->SetBranchAddress("Event",&Event);

        
        const Int_t nentries = (Int_t)current_sample->tree->GetEntries();
        std::cout << "Events in sample:" << nentries << std::endl;

        for (int i=0; i < nentries; i++){

            current_sample->tree->GetEntry(i);
            for (int i = 0; i < 20; i++){
                histograms["mass_weighted"]->Fill(jtrip_mass[i], current_sample->weight);
                histograms["mass_unweighted"]->Fill(jtrip_mass[i]);
            }
            
        }

        current_sample->tree->ResetBranchAddresses();


    }

    output_hists->Write();



}