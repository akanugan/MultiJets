#ifndef Analyzer_H
#define Analyzer_H

#include <iostream>
#include <fstream>
#include <cmath>
#include <vector>
#include "events.h"
#include "TH1F.h"
#include "TH2.h"
#include <TProfile.h>
#include "TFile.h"
#include "TLorentzVector.h"
#include "TDirectory.h"
#include <vector>

using namespace std;

class Analyzer : public events{

public:
Analyzer(const TString &inputFileList="foo.txt", const char *outFileName="histo.root",const char *dataset="data");
~Analyzer();
Bool_t   FillChain(TChain *chain, const TString &inputFileList);
Long64_t LoadTree(Long64_t entry);
void     CopyCutFlow();
void     EventLoop(const char *,const char *);
void     BookHistogram(const char *);
void print(Long64_t);

//Variables defined
bool isMC=true;
double deepCSVvalue = 0;

TH1F *h_cutflow;
TH1F *old_cutflow;
TH1D *hist_region_1;
TH1D *hist_region_2;
TH1D *hist_region_3;
TH1D *ht_plot;


// TH1D *h_b_Run;  
// TH1D *h_b_Lumi;   
// TH1D *h_b_Event;   
// TH1D *h_b_xscn;   
// TH1D *h_b_trigger_results;
// TH1D *h_b_mds63;  
// TH1D *h_b_mds6332;   
// TH1D *h_b_jmds63;   
// TH1D *h_b_jmds6332;  
// TH1D *h_b_sixpt;   
// TH1D *h_b_ak4_HT;   
// TH1D *h_b_loose6j_qgl;;
// TH1D *h_b_tight6j_qgl;
// TH1D *h_b_net_tight_qgl;
// TH1D *h_b_ak4_num;   
// TH1D *h_b_trip_num;  
// TH1D *h_b_pmds63;   
// TH1D *h_b_pmds6332;  
// TH1D *h_b_ak4_pt;   
// TH1D *h_b_ak4_eta;   
// TH1D *h_b_ak4_phi;   
// TH1D *h_b_ak4_m;   
// TH1D *h_b_ak4_area;  
// TH1D *h_b_ak4_jec;   
// TH1D *h_b_ak4_csv;   
// TH1D *h_b_ak4_jetid; 
// TH1D *h_b_ak4_match; 
// TH1D *h_b_ak4_qgl;   
// TH1D *h_b_trip_mass; 
// TH1D *h_b_trip_vpt;  
// TH1D *h_b_trip_spt;  
// TH1D *h_b_trip_delta;
// TH1D *h_b_trip_eta;  
// TH1D *h_b_trip_phi;  
// TH1D *h_b_trip_masym;
// TH1D *h_b_trip_deta; 
// TH1D *h_b_trip_mds;  
// TH1D *h_b_trip_dlow; 
// TH1D *h_b_trip_dmid; 
// TH1D *h_b_trip_dhigh;
// TH1D *h_b_trip_match;
// TH1D *h_b_trip_tpind;
// TH1D *h_b_trip_jind; 
// TH1D *h_b_trip_csv;  
// TH1D *h_b_trip_m63;  
TH1D *h_b_jtrip_mass;
TH1D *h_b_jtrip_vpt; 
TH1D *h_b_jtrip_spt; 
TH1D *h_b_jtrip_delta;
TH1D *h_b_jtrip_eta; 
TH1D *h_b_jtrip_phi; 
TH1D *h_b_jtrip_masym;
TH1D *h_b_jtrip_deta;
TH1D *h_b_jtrip_mds; 
TH1D *h_b_jtrip_dlow;
TH1D *h_b_jtrip_dmid;
TH1D *h_b_jtrip_dhigh;
TH1D *h_b_jtrip_match;
TH1D *h_b_jtrip_tpind;
TH1D *h_b_jtrip_jind;
TH1D *h_b_jtrip_csv; 
TH1D *h_b_jtrip_m63; 
TH1D *h_b_trip_qgl;  
TH1D *h_b_trip_qgt;  
TH1D *h_b_jtrip_qgl; 
TH1D *h_b_jtrip_qgt; 
// TH1D *h_b_ptrip_mass;
// TH1D *h_b_ptrip_vpt; 
// TH1D *h_b_ptrip_spt; 
// TH1D *h_b_ptrip_delta;
// TH1D *h_b_ptrip_eta; 
// TH1D *h_b_ptrip_phi; 
// TH1D *h_b_ptrip_masym;
// TH1D *h_b_ptrip_deta;
// TH1D *h_b_ptrip_mds; 
// TH1D *h_b_ptrip_dlow;
// TH1D *h_b_ptrip_dmid;
// TH1D *h_b_ptrip_dhigh;
// TH1D *h_b_ptrip_match;
// TH1D *h_b_ptrip_tpind;
// TH1D *h_b_ptrip_jind;
// TH1D *h_b_ptrip_csv; 
// TH1D *h_b_ptrip_m63; 
// TH1D *h_b_ptrip_qgl; 
// TH1D *h_b_ptrip_qgt; 


TFile *oFile;
  
};
#endif

#ifdef Analyzer_cxx

void Analyzer::BookHistogram(const char *outFileName) {

    //  char hname[200], htit[200];
    //  double xlow = 0.0,  xhigh = 2000.0;
    //  int nbins = 2000;
    TString name,title;

    oFile = new TFile(outFileName, "recreate");
    TH1::SetDefaultSumw2(1);


    h_cutflow = new TH1F("CutFlow","cut flow",25,0,25);
    hist_region_1 = new TH1D("hist_region_1", "Region 1 Histogram", 102 * 2, 300, 1200);
    hist_region_2 = new TH1D("hist_region_2", "Region 2 Histogram", 90 * 2, 300, 1200);
    hist_region_3 = new TH1D("hist_region_3", "Region 3 Histogram", 99 * 2, 300, 1200);
    ht_plot = new TH1D("ht_plot", "HT", 99 * 2, 0, 2500);
    
    // h_b_Run  = new TH1D("h_b_Run", "Run",50,0,100); 
    // h_b_Lumi = new TH1D("h_b_Lumi", "Lumi",50,0,100);   
    // h_b_Event = new TH1D("h_b_Event", "Event",50,0,100);   
    // h_b_xscn = new TH1D("h_b_xscn", "xscn",50,0,100);   
    // h_b_trigger_results = new TH1D("h_b_trigger_results","trigger_results",50,0,100);
    // h_b_mds63 = new TH1D("   h_b_mds63", "mds63",50,0,100);
    // h_b_mds6332 = new TH1D("h_b_mds6332;", "mds6332;",50,0,100);  
    // h_b_jmds63 = new TH1D(" h_b_jmds63;", "jmds63;",50,0,100);
    // h_b_jmds6332 = new TH1D("h_b_jmds6332", "jmds6332",50,0,100);  
    // h_b_sixpt = new TH1D("h_b_sixpsixpt", "sixpsixpt", 50, 0, 100);   
    // h_b_ak4_HT = new TH1D("h_b_ak4_HT", "ak4_HT", 50, 0, 100);   
    // h_b_loose6j_qgl = new TH1D("h_b_loose6j_qgl", " oose6j_qgl", 50, 0, 100);
    // h_b_tight6j_qgl = new TH1D("h_b_tight6j_qgl", "tight6j_qgl", 50, 0, 100);
    // h_b_net_tight_qgl = new TH1D("h_b_net_tight_qgl", "net_tight_qgl", 50, 0, 100);
    // h_b_ak4_num = new TH1D("h_b_ak4_num", "ak4_num", 50, 0, 100);   
    // h_b_trip_num = new TH1D("h_b_trip_num", "trip_num", 50, 0, 100);  
    // h_b_pmds63 = new TH1D("h_b_pmds63", "pmds63", 50, 0, 100);   
    // h_b_pmds6332 = new TH1D("h_b_pmds6332", "pmds6332", 50, 0, 100);  
    // h_b_ak4_pt = new TH1D("h_b_ak4_pt", "ak4_pt", 50, 0, 100);   
    // h_b_ak4_eta = new TH1D("h_b_ak4_eta", "ak4_eta", 50, 0, 100);   
    // h_b_ak4_phi = new TH1D("h_b_ak4_phi", "ak4_phi", 50, 0, 100);   
    // h_b_ak4_m = new TH1D("h_b_ak4_m", "ak4_m", 50, 0, 100);   
    // h_b_ak4_area = new TH1D("h_b_ak4_area", "ak4_area", 50, 0, 100);  
    // h_b_ak4_jec = new TH1D("h_b_ak4_jec", "ak4_jec", 50, 0, 100);   
    // h_b_ak4_csv = new TH1D("h_b_ak4_csv", "ak4_csv", 50, 0, 100);   
    // h_b_ak4_jetid = new TH1D("h_b_ak4_jetid", "ak4_jetid", 50, 0, 100); 
    // h_b_ak4_match = new TH1D("h_b_ak4_match", "ak4_match", 50, 0, 100); 
    // h_b_ak4_qgl = new TH1D("h_b_ak4_qgl", "ak4_qgl", 50, 0, 100);   
    // h_b_trip_mass = new TH1D("h_b_trip_mass", "trip_mass", 25, 0, 3000); 
    // h_b_trip_vpt = new TH1D("h_b_trip_vpt", "trip_vpt", 25, 0, 500);  
    // h_b_trip_spt = new TH1D("h_b_trip_spt", "trip_spt", 25, 0, 100);  
    // h_b_trip_delta = new TH1D("h_b_trip_delta", "trip_delta", 25, -2000, 2000);
    // h_b_trip_eta = new TH1D("h_b_trip_eta", "trip_eta", 25, -7, 7);  
    // h_b_trip_phi = new TH1D("h_b_trip_phi", "trip_phi", 25, -3.5, 3.5);  
    // h_b_trip_masym = new TH1D("h_b_trip_masym", "trip_masym", 25, 0, 1),
    // h_b_trip_deta = new TH1D("h_b_trip_deta", "trip_deta", 25, 0, 100); 
    // h_b_trip_mds = new TH1D("h_b_trip_mds", "trip_mds", 25, 0, 1);  
    // h_b_trip_dlow = new TH1D("h_b_trip_dlow", "trip_dlow", 25, 0, 1); 
    // h_b_trip_dmid = new TH1D("h_b_trip_dmid", "trip_dmid", 25, 0, 1); 
    // h_b_trip_dhigh = new TH1D("h_b_trip_dhigh", "trip_dhigh", 25, 0, 1);
    // h_b_trip_match = new TH1D("h_b_trip_match", "trip_match", 25, 0, 100);
    // h_b_trip_tpind = new TH1D("h_b_trip_tpind", "trip_tpind", 25, 0, 1000);
    // h_b_trip_jind = new TH1D("h_b_trip_jind", "trip_jind", 25, 0, 1000); 
    // h_b_trip_csv = new TH1D("h_b_trip_csv", "trip_csv", 25, 0, 1);  
    // h_b_trip_m63 = new TH1D("h_b_trip_m63", "trip_m63", 25, 0, 1);  
    // h_b_trip_qgl = new TH1D("h_b_trip_qgl", "trip_qgl", 25, 0, 1);  
    // h_b_trip_qgt = new TH1D("h_b_trip_qgt", "trip_qgt", 25, 0, 1); 

    h_b_jtrip_mass = new TH1D("h_b_jtrip_mass", "jtrip_mass", 25, 0, 3000); 
    h_b_jtrip_vpt = new TH1D("h_b_jtrip_vpt", "jtrip_vpt", 25, 0, 500);  
    h_b_jtrip_spt = new TH1D("h_b_jtrip_spt", "jtrip_spt", 25, 0, 100);  
    h_b_jtrip_delta = new TH1D("h_b_jtrip_delta", "jtrip_delta", 25, -2000, 2000);
    h_b_jtrip_eta = new TH1D("h_b_jtrip_eta", "jtrip_eta", 25, -7, 7);  
    h_b_jtrip_phi = new TH1D("h_b_jtrip_phi", "jtrip_phi", 25, -3.5, 3.5);  
    h_b_jtrip_masym = new TH1D("h_b_jtrip_masym", "jtrip_masym", 25, 0, 1),
    h_b_jtrip_deta = new TH1D("h_b_jtrip_deta", "jtrip_deta", 25, 0, 100); 
    h_b_jtrip_mds = new TH1D("h_b_jtrip_mds", "jtrip_mds", 25, 0, 1);  
    h_b_jtrip_dlow = new TH1D("h_b_jtrip_dlow", "jtrip_dlow", 25, 0, 1); 
    h_b_jtrip_dmid = new TH1D("h_b_jtrip_dmid", "jtrip_dmid", 25, 0, 1); 
    h_b_jtrip_dhigh = new TH1D("h_b_jtrip_dhigh", "jtrip_dhigh", 25, 0, 1);
    h_b_jtrip_match = new TH1D("h_b_jtrip_match", "jtrip_match", 25, 0, 100);
    h_b_jtrip_tpind = new TH1D("h_b_jtrip_tpind", "tjrip_tpind", 25, 0, 1000);
    h_b_jtrip_jind = new TH1D("h_b_jtrip_jind", "jtrip_jind", 25, 0, 1000); 
    h_b_jtrip_csv = new TH1D("h_b_jtrip_csv", "jtrip_csv", 25, 0, 1);  
    h_b_jtrip_m63 = new TH1D("h_b_jtrip_m63", "jtrip_m63", 25, 0, 1);  
    h_b_jtrip_qgl = new TH1D("h_b_jtrip_qgl", "jtrip_qgl", 25, 0, 1);  
    h_b_jtrip_qgt = new TH1D("h_b_jtrip_qgt", "jtrip_qgt", 25, 0, 1);    

    // h_b_ptrip_mass = new TH1D("h_b_ptrip_mass", "ptrip_mass", 25, 0, 3000); 
    // h_b_ptrip_vpt = new TH1D("h_b_ptrip_vpt", "ptrip_vpt", 25, 0, 500);  
    // h_b_ptrip_spt = new TH1D("h_b_ptrip_spt", "ptrip_spt", 25, 0, 100);  
    // h_b_ptrip_delta = new TH1D("h_b_ptrip_delta", "ptrip_delta", 25, -2000, 2000);
    // h_b_ptrip_eta = new TH1D("h_b_ptrip_eta", "ptrip_eta", 25, -7, 7);  
    // h_b_ptrip_phi = new TH1D("h_b_ptrip_phi", "ptrip_phi", 25, -3.5, 3.5);  
    // h_b_ptrip_masym = new TH1D("h_b_ptrip_masym", "ptrip_masym", 25, 0, 1),
    // h_b_ptrip_deta = new TH1D("h_b_ptrip_deta", "ptrip_deta", 25, 0, 100); 
    // h_b_ptrip_mds = new TH1D("h_b_ptrip_mds", "ptrip_mds", 25, 0, 1);  
    // h_b_ptrip_dlow = new TH1D("h_b_ptrip_dlow", "ptrip_dlow", 25, 0, 1); 
    // h_b_ptrip_dmid = new TH1D("h_b_ptrip_dmid", "ptrip_dmid", 25, 0, 1); 
    // h_b_ptrip_dhigh = new TH1D("h_b_ptrip_dhigh", "ptrip_dhigh", 25, 0, 1);
    // h_b_ptrip_match = new TH1D("h_b_ptrip_match", "ptrip_match", 25, 0, 100);
    // h_b_ptrip_tpind = new TH1D("h_b_ptrip_tpind", "ptrip_tpind", 25, 0, 1000);
    // h_b_ptrip_jind = new TH1D("h_b_ptrip_jind", "ptrip_jind", 25, 0, 1000); 
    // h_b_ptrip_csv = new TH1D("h_b_ptrip_csv", "ptrip_csv", 25, 0, 1);  
    // h_b_ptrip_m63 = new TH1D("h_b_ptrip_m63", "ptrip_m63", 25, 0, 1);  
    // h_b_ptrip_qgl = new TH1D("h_b_ptrip_qgl", "ptrip_qgl", 25, 0, 1);  
    // h_b_ptrip_qgt = new TH1D("h_b_ptrip_qgt", "ptrip_qgt", 25, 0, 1); 
}

void Analyzer::CopyCutFlow() {
    TChain *file = (TChain*) fChain;
    TH1F  *old_cut_flow = file->GetFile()->Get<TH1F>("cut_flow_hist");
    if (old_cut_flow)
    {
      old_cutflow = new TH1F(*old_cut_flow);
    }
}
  

Analyzer::Analyzer(const TString &inputFileList, const char *outFileName, const char* dataset) {
  string nameData=dataset;
  TString nameData2 = nameData;
  TChain *tree = new TChain("events");
  if( ! FillChain(tree, inputFileList) ) {
    std::cerr << "Cannot get the tree " << std::endl;
  } else {
    std::cout << "Initiating Analysis of dataset " << dataset << std::endl;
  }

  cout<<"Treating the input files as "<<nameData<<" for setting tree branches"<<endl;
  events::Init(tree,nameData);
  BookHistogram(outFileName);
  
}

Bool_t Analyzer::FillChain(TChain *chain, const TString &inputFileList) {
  int itr=0;
  TFile *filePointer;
  ifstream infile(inputFileList, ifstream::in);
  //std::string buffer;

  if(!infile.is_open()) {
    std::cerr << "** ERROR: Can't open '" << inputFileList << "' for input" << std::endl;
    return kFALSE;
  }

  std::cout << "TreeUtilities : FillChain " << std::endl;
  
  //infile >> buffer;
  //if(!infile.good()) break;
  for (string line; getline(infile, line); ){
    std::cout << "Adding tree from " << line.c_str() << std::endl;
    chain->Add(line.c_str());
  }

  
  std::cout << "No. of Entries in this tree : " << chain->GetEntries() << std::endl;
  return kTRUE;
}

Long64_t Analyzer::LoadTree(Long64_t entry) {
  // Set the environment to read one entry                                                                                          
  if (!fChain) return -5;
  Long64_t centry = fChain->LoadTree(entry);
  if (centry < 0) return centry;
  if (!fChain->InheritsFrom(TChain::Class()))  return centry;
  TChain *chain = (TChain*)fChain;
  if (chain->GetTreeNumber() != fCurrent) {
    fCurrent = chain->GetTreeNumber();
    //    Notify();
  }
  return centry;
}

Analyzer::~Analyzer() { 

  if (!fChain) return;
  delete fChain->GetCurrentFile();
  oFile->cd();
  oFile->Write();
  oFile->Close();

}

#endif
