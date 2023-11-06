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
void     EventLoop(const char *,const char *);
void     BookHistogram(const char *);
void print(Long64_t);

//Variables defined
bool isMC=true;
double deepCSVvalue = 0;

TH1F *h_cutflow;
TH1D *hist_region_1;
TH1D *hist_region_2;
TH1D *hist_region_3;


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
    hist_region_1 = new TH1D("hist_region_1", "Region 1 Histogram", 102 * 2, 100, 610);
    hist_region_2 = new TH1D("hist_region_2", "Region 2 Histogram", 90 * 2, 300, 1200);
    hist_region_3 = new TH1D("hist_region_3", "Region 3 Histogram", 99 * 2, 520, 2500);
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
  std::string buffer;

  if(!infile.is_open()) {
    std::cerr << "** ERROR: Can't open '" << inputFileList << "' for input" << std::endl;
    return kFALSE;
  }

  std::cout << "TreeUtilities : FillChain " << std::endl;
  
  infile >> buffer;
  //if(!infile.good()) break;
  std::cout << "Adding tree from " << buffer.c_str() << std::endl;
  chain->Add(buffer.c_str());

  
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