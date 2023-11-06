//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Mon Nov  6 11:49:18 2023 by ROOT version 6.12/07
// from TTree events/tree with jets
// found on file: test/slimmedNtup_slimmed_ntuple_QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8_v1_1-1.root
//////////////////////////////////////////////////////////

#ifndef events_h
#define events_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <TSelector.h>
#include <vector>
#include <TLorentzVector.h>


// Header file for the classes stored in the TTree if any.

using namespace std;
class events {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

// Fixed size dimensions of array or collections stored in the TTree if any.

   // Declaration of leaf types
   Float_t         Run;
   Float_t         Lumi;
   Float_t         Event;
   Float_t         xscn;
   Float_t         trigger_results;
   Float_t         mds63;
   Float_t         mds6332;
   Float_t         jmds63;
   Float_t         jmds6332;
   Float_t         sixpt;
   Float_t         ak4_HT;
   Float_t         loose6j_qgl;
   Float_t         tight6j_qgl;
   Float_t         net_tight_qgl;
   Int_t           ak4_num;
   Int_t           trip_num;
   Float_t         pmds63;
   Float_t         pmds6332;
   Float_t         ak4_pt[8];   //[ak4_num]
   Float_t         ak4_eta[8];   //[ak4_num]
   Float_t         ak4_phi[8];   //[ak4_num]
   Float_t         ak4_m[8];   //[ak4_num]
   Float_t         ak4_area[8];   //[ak4_num]
   Float_t         ak4_jec[8];   //[ak4_num]
   Float_t         ak4_csv[8];   //[ak4_num]
   Float_t         ak4_jetid[8];   //[ak4_num]
   Float_t         ak4_match[8];   //[ak4_num]
   Float_t         ak4_qgl[8];   //[ak4_num]
   Float_t         trip_mass[20];   //[trip_num]
   Float_t         trip_vpt[20];   //[trip_num]
   Float_t         trip_spt[20];   //[trip_num]
   Float_t         trip_delta[20];   //[trip_num]
   Float_t         trip_eta[20];   //[trip_num]
   Float_t         trip_phi[20];   //[trip_num]
   Float_t         trip_masym[20];   //[trip_num]
   Float_t         trip_deta[20];   //[trip_num]
   Float_t         trip_mds[20];   //[trip_num]
   Float_t         trip_dlow[20];   //[trip_num]
   Float_t         trip_dmid[20];   //[trip_num]
   Float_t         trip_dhigh[20];   //[trip_num]
   Float_t         trip_match[20];   //[trip_num]
   Float_t         trip_tpind[20];   //[trip_num]
   Float_t         trip_jind[20];   //[trip_num]
   Float_t         trip_csv[20];   //[trip_num]
   Float_t         trip_m63[20];   //[trip_num]
   Float_t         jtrip_mass[20];   //[trip_num]
   Float_t         jtrip_vpt[20];   //[trip_num]
   Float_t         jtrip_spt[20];   //[trip_num]
   Float_t         jtrip_delta[20];   //[trip_num]
   Float_t         jtrip_eta[20];   //[trip_num]
   Float_t         jtrip_phi[20];   //[trip_num]
   Float_t         jtrip_masym[20];   //[trip_num]
   Float_t         jtrip_deta[20];   //[trip_num]
   Float_t         jtrip_mds[20];   //[trip_num]
   Float_t         jtrip_dlow[20];   //[trip_num]
   Float_t         jtrip_dmid[20];   //[trip_num]
   Float_t         jtrip_dhigh[20];   //[trip_num]
   Float_t         jtrip_match[20];   //[trip_num]
   Float_t         jtrip_tpind[20];   //[trip_num]
   Float_t         jtrip_jind[20];   //[trip_num]
   Float_t         jtrip_csv[20];   //[trip_num]
   Float_t         jtrip_m63[20];   //[trip_num]
   Float_t         trip_qgl[20];   //[trip_num]
   Float_t         trip_qgt[20];   //[trip_num]
   Float_t         jtrip_qgl[20];   //[trip_num]
   Float_t         jtrip_qgt[20];   //[trip_num]
   Float_t         ptrip_mass[20];   //[trip_num]
   Float_t         ptrip_vpt[20];   //[trip_num]
   Float_t         ptrip_spt[20];   //[trip_num]
   Float_t         ptrip_delta[20];   //[trip_num]
   Float_t         ptrip_eta[20];   //[trip_num]
   Float_t         ptrip_phi[20];   //[trip_num]
   Float_t         ptrip_masym[20];   //[trip_num]
   Float_t         ptrip_deta[20];   //[trip_num]
   Float_t         ptrip_mds[20];   //[trip_num]
   Float_t         ptrip_dlow[20];   //[trip_num]
   Float_t         ptrip_dmid[20];   //[trip_num]
   Float_t         ptrip_dhigh[20];   //[trip_num]
   Float_t         ptrip_match[20];   //[trip_num]
   Float_t         ptrip_tpind[20];   //[trip_num]
   Float_t         ptrip_pind[20];   //[trip_num]
   Float_t         ptrip_csv[20];   //[trip_num]
   Float_t         ptrip_m63[20];   //[trip_num]
   Float_t         ptrip_qgl[20];   //[trip_num]
   Float_t         ptrip_qgt[20];   //[trip_num]

   // List of branches
   TBranch        *b_Run;   //!
   TBranch        *b_Lumi;   //!
   TBranch        *b_Event;   //!
   TBranch        *b_xscn;   //!
   TBranch        *b_trigger_results;   //!
   TBranch        *b_mds63;   //!
   TBranch        *b_mds6332;   //!
   TBranch        *b_jmds63;   //!
   TBranch        *b_jmds6332;   //!
   TBranch        *b_sixpt;   //!
   TBranch        *b_ak4_HT;   //!
   TBranch        *b_loose6j_qgl;   //!
   TBranch        *b_tight6j_qgl;   //!
   TBranch        *b_net_tight_qgl;   //!
   TBranch        *b_ak4_num;   //!
   TBranch        *b_trip_num;   //!
   TBranch        *b_pmds63;   //!
   TBranch        *b_pmds6332;   //!
   TBranch        *b_ak4_pt;   //!
   TBranch        *b_ak4_eta;   //!
   TBranch        *b_ak4_phi;   //!
   TBranch        *b_ak4_m;   //!
   TBranch        *b_ak4_area;   //!
   TBranch        *b_ak4_jec;   //!
   TBranch        *b_ak4_csv;   //!
   TBranch        *b_ak4_jetid;   //!
   TBranch        *b_ak4_match;   //!
   TBranch        *b_ak4_qgl;   //!
   TBranch        *b_trip_mass;   //!
   TBranch        *b_trip_vpt;   //!
   TBranch        *b_trip_spt;   //!
   TBranch        *b_trip_delta;   //!
   TBranch        *b_trip_eta;   //!
   TBranch        *b_trip_phi;   //!
   TBranch        *b_trip_masym;   //!
   TBranch        *b_trip_deta;   //!
   TBranch        *b_trip_mds;   //!
   TBranch        *b_trip_dlow;   //!
   TBranch        *b_trip_dmid;   //!
   TBranch        *b_trip_dhigh;   //!
   TBranch        *b_trip_match;   //!
   TBranch        *b_trip_tpind;   //!
   TBranch        *b_trip_jind;   //!
   TBranch        *b_trip_csv;   //!
   TBranch        *b_trip_m63;   //!
   TBranch        *b_jtrip_mass;   //!
   TBranch        *b_jtrip_vpt;   //!
   TBranch        *b_jtrip_spt;   //!
   TBranch        *b_jtrip_delta;   //!
   TBranch        *b_jtrip_eta;   //!
   TBranch        *b_jtrip_phi;   //!
   TBranch        *b_jtrip_masym;   //!
   TBranch        *b_jtrip_deta;   //!
   TBranch        *b_jtrip_mds;   //!
   TBranch        *b_jtrip_dlow;   //!
   TBranch        *b_jtrip_dmid;   //!
   TBranch        *b_jtrip_dhigh;   //!
   TBranch        *b_jtrip_match;   //!
   TBranch        *b_jtrip_tpind;   //!
   TBranch        *b_jtrip_jind;   //!
   TBranch        *b_jtrip_csv;   //!
   TBranch        *b_jtrip_m63;   //!
   TBranch        *b_trip_qgl;   //!
   TBranch        *b_trip_qgt;   //!
   TBranch        *b_jtrip_qgl;   //!
   TBranch        *b_jtrip_qgt;   //!
   TBranch        *b_ptrip_mass;   //!
   TBranch        *b_ptrip_vpt;   //!
   TBranch        *b_ptrip_spt;   //!
   TBranch        *b_ptrip_delta;   //!
   TBranch        *b_ptrip_eta;   //!
   TBranch        *b_ptrip_phi;   //!
   TBranch        *b_ptrip_masym;   //!
   TBranch        *b_ptrip_deta;   //!
   TBranch        *b_ptrip_mds;   //!
   TBranch        *b_ptrip_dlow;   //!
   TBranch        *b_ptrip_dmid;   //!
   TBranch        *b_ptrip_dhigh;   //!
   TBranch        *b_ptrip_match;   //!
   TBranch        *b_ptrip_tpind;   //!
   TBranch        *b_ptrip_pind;   //!
   TBranch        *b_ptrip_csv;   //!
   TBranch        *b_ptrip_m63;   //!
   TBranch        *b_ptrip_qgl;   //!
   TBranch        *b_ptrip_qgt;   //!

   events(TTree * /*tree*/ =0) : fChain(0) { }
   virtual ~events();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void    Init(TTree *tree, string);
   //virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
   double  DeltaPhi(double, double);
   double  DeltaR(double eta1, double phi1, double eta2, double phi2);
   void    sortTLorVec(vector<TLorentzVector> *);   
};

#endif

#ifdef events_cxx

// events::events(TTree *tree) : fChain(0) 
// {
// // if parameter tree is not specified (or zero), connect the file
// // used to generate this class and read the Tree.
//    if (tree == 0) {
//       TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("test/slimmedNtup_slimmed_ntuple_QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8_v1_1-1.root");
//       if (!f || !f->IsOpen()) {
//          f = new TFile("test/slimmedNtup_slimmed_ntuple_QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8_v1_1-1.root");
//       }
//       f->GetObject("events",tree);

//    }
//    Init(tree);
// }

events::~events()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t events::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t events::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void events::Init(TTree *tree, string nameData)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("Run", &Run, &b_Run);
   fChain->SetBranchAddress("Lumi", &Lumi, &b_Lumi);
   fChain->SetBranchAddress("Event", &Event, &b_Event);
   fChain->SetBranchAddress("xscn", &xscn, &b_xscn);
   fChain->SetBranchAddress("trigger_results", &trigger_results, &b_trigger_results);
   fChain->SetBranchAddress("mds63", &mds63, &b_mds63);
   fChain->SetBranchAddress("mds6332", &mds6332, &b_mds6332);
   fChain->SetBranchAddress("jmds63", &jmds63, &b_jmds63);
   fChain->SetBranchAddress("jmds6332", &jmds6332, &b_jmds6332);
   fChain->SetBranchAddress("sixpt", &sixpt, &b_sixpt);
   fChain->SetBranchAddress("ak4_HT", &ak4_HT, &b_ak4_HT);
   fChain->SetBranchAddress("loose6j_qgl", &loose6j_qgl, &b_loose6j_qgl);
   fChain->SetBranchAddress("tight6j_qgl", &tight6j_qgl, &b_tight6j_qgl);
   fChain->SetBranchAddress("net_tight_qgl", &net_tight_qgl, &b_net_tight_qgl);
   fChain->SetBranchAddress("ak4_num", &ak4_num, &b_ak4_num);
   fChain->SetBranchAddress("trip_num", &trip_num, &b_trip_num);
   fChain->SetBranchAddress("pmds63", &pmds63, &b_pmds63);
   fChain->SetBranchAddress("pmds6332", &pmds6332, &b_pmds6332);
   fChain->SetBranchAddress("ak4_pt", ak4_pt, &b_ak4_pt);
   fChain->SetBranchAddress("ak4_eta", ak4_eta, &b_ak4_eta);
   fChain->SetBranchAddress("ak4_phi", ak4_phi, &b_ak4_phi);
   fChain->SetBranchAddress("ak4_m", ak4_m, &b_ak4_m);
   fChain->SetBranchAddress("ak4_area", ak4_area, &b_ak4_area);
   fChain->SetBranchAddress("ak4_jec", ak4_jec, &b_ak4_jec);
   fChain->SetBranchAddress("ak4_csv", ak4_csv, &b_ak4_csv);
   fChain->SetBranchAddress("ak4_jetid", ak4_jetid, &b_ak4_jetid);
   fChain->SetBranchAddress("ak4_match", ak4_match, &b_ak4_match);
   fChain->SetBranchAddress("ak4_qgl", ak4_qgl, &b_ak4_qgl);
   fChain->SetBranchAddress("trip_mass", trip_mass, &b_trip_mass);
   fChain->SetBranchAddress("trip_vpt", trip_vpt, &b_trip_vpt);
   fChain->SetBranchAddress("trip_spt", trip_spt, &b_trip_spt);
   fChain->SetBranchAddress("trip_delta", trip_delta, &b_trip_delta);
   fChain->SetBranchAddress("trip_eta", trip_eta, &b_trip_eta);
   fChain->SetBranchAddress("trip_phi", trip_phi, &b_trip_phi);
   fChain->SetBranchAddress("trip_masym", trip_masym, &b_trip_masym);
   fChain->SetBranchAddress("trip_deta", trip_deta, &b_trip_deta);
   fChain->SetBranchAddress("trip_mds", trip_mds, &b_trip_mds);
   fChain->SetBranchAddress("trip_dlow", trip_dlow, &b_trip_dlow);
   fChain->SetBranchAddress("trip_dmid", trip_dmid, &b_trip_dmid);
   fChain->SetBranchAddress("trip_dhigh", trip_dhigh, &b_trip_dhigh);
   fChain->SetBranchAddress("trip_match", trip_match, &b_trip_match);
   fChain->SetBranchAddress("trip_tpind", trip_tpind, &b_trip_tpind);
   fChain->SetBranchAddress("trip_jind", trip_jind, &b_trip_jind);
   fChain->SetBranchAddress("trip_csv", trip_csv, &b_trip_csv);
   fChain->SetBranchAddress("trip_m63", trip_m63, &b_trip_m63);
   fChain->SetBranchAddress("jtrip_mass", jtrip_mass, &b_jtrip_mass);
   fChain->SetBranchAddress("jtrip_vpt", jtrip_vpt, &b_jtrip_vpt);
   fChain->SetBranchAddress("jtrip_spt", jtrip_spt, &b_jtrip_spt);
   fChain->SetBranchAddress("jtrip_delta", jtrip_delta, &b_jtrip_delta);
   fChain->SetBranchAddress("jtrip_eta", jtrip_eta, &b_jtrip_eta);
   fChain->SetBranchAddress("jtrip_phi", jtrip_phi, &b_jtrip_phi);
   fChain->SetBranchAddress("jtrip_masym", jtrip_masym, &b_jtrip_masym);
   fChain->SetBranchAddress("jtrip_deta", jtrip_deta, &b_jtrip_deta);
   fChain->SetBranchAddress("jtrip_mds", jtrip_mds, &b_jtrip_mds);
   fChain->SetBranchAddress("jtrip_dlow", jtrip_dlow, &b_jtrip_dlow);
   fChain->SetBranchAddress("jtrip_dmid", jtrip_dmid, &b_jtrip_dmid);
   fChain->SetBranchAddress("jtrip_dhigh", jtrip_dhigh, &b_jtrip_dhigh);
   fChain->SetBranchAddress("jtrip_match", jtrip_match, &b_jtrip_match);
   fChain->SetBranchAddress("jtrip_tpind", jtrip_tpind, &b_jtrip_tpind);
   fChain->SetBranchAddress("jtrip_jind", jtrip_jind, &b_jtrip_jind);
   fChain->SetBranchAddress("jtrip_csv", jtrip_csv, &b_jtrip_csv);
   fChain->SetBranchAddress("jtrip_m63", jtrip_m63, &b_jtrip_m63);
   fChain->SetBranchAddress("trip_qgl", trip_qgl, &b_trip_qgl);
   fChain->SetBranchAddress("trip_qgt", trip_qgt, &b_trip_qgt);
   fChain->SetBranchAddress("jtrip_qgl", jtrip_qgl, &b_jtrip_qgl);
   fChain->SetBranchAddress("jtrip_qgt", jtrip_qgt, &b_jtrip_qgt);
   fChain->SetBranchAddress("ptrip_mass", ptrip_mass, &b_ptrip_mass);
   fChain->SetBranchAddress("ptrip_vpt", ptrip_vpt, &b_ptrip_vpt);
   fChain->SetBranchAddress("ptrip_spt", ptrip_spt, &b_ptrip_spt);
   fChain->SetBranchAddress("ptrip_delta", ptrip_delta, &b_ptrip_delta);
   fChain->SetBranchAddress("ptrip_eta", ptrip_eta, &b_ptrip_eta);
   fChain->SetBranchAddress("ptrip_phi", ptrip_phi, &b_ptrip_phi);
   fChain->SetBranchAddress("ptrip_masym", ptrip_masym, &b_ptrip_masym);
   fChain->SetBranchAddress("ptrip_deta", ptrip_deta, &b_ptrip_deta);
   fChain->SetBranchAddress("ptrip_mds", ptrip_mds, &b_ptrip_mds);
   fChain->SetBranchAddress("ptrip_dlow", ptrip_dlow, &b_ptrip_dlow);
   fChain->SetBranchAddress("ptrip_dmid", ptrip_dmid, &b_ptrip_dmid);
   fChain->SetBranchAddress("ptrip_dhigh", ptrip_dhigh, &b_ptrip_dhigh);
   fChain->SetBranchAddress("ptrip_match", ptrip_match, &b_ptrip_match);
   fChain->SetBranchAddress("ptrip_tpind", ptrip_tpind, &b_ptrip_tpind);
   fChain->SetBranchAddress("ptrip_pind", ptrip_pind, &b_ptrip_pind);
   fChain->SetBranchAddress("ptrip_csv", ptrip_csv, &b_ptrip_csv);
   fChain->SetBranchAddress("ptrip_m63", ptrip_m63, &b_ptrip_m63);
   fChain->SetBranchAddress("ptrip_qgl", ptrip_qgl, &b_ptrip_qgl);
   fChain->SetBranchAddress("ptrip_qgt", ptrip_qgt, &b_ptrip_qgt);
   Notify();
}

Bool_t events::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void events::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t events::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef events_cxx
