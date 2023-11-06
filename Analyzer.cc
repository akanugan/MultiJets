#define Analyzer_cxx
#include "Analyzer.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TLorentzVector.h>
#include <iostream>
#include <vector>
#include <cstring>
#include <string>
#include <tuple>
#include <fstream>

using namespace std;
//
int main(int argc, char* argv[])
{

if (argc < 2) {
   cerr << "Please give 3 arguments " << "runList " << " " << "outputFileName" << " " << "dataset" << endl;
   return -1;
}
const char *inputFileList = argv[1];
const char *outFileName   = argv[2];
const char *data          = argv[3];

Analyzer ana(inputFileList, outFileName, data);
cout << "dataset " << data << " " << endl;
cout << "input File: " << inputFileList << " " << endl;
vector<double> mass;
int idx;
ana.EventLoop(data,inputFileList);
return 0;
}

void Analyzer::EventLoop(const char *data,const char *inputFileList) {
  if (fChain == 0) return;

  Long64_t nentries = fChain->GetEntriesFast();
  cout << "nentries " << nentries << endl;
  cout << "Analyzing dataset " << data << " " << endl;

  TString s_data=data;
  Long64_t nbytes = 0, nb = 0;
  int decade = 0;
  //if(dataRun>0) cout<<"Processing it as "<<dataRun<<" data"<<endl;
  //else if(dataRun<0) cout<<"Processing it as "<<abs(dataRun)<<" MC"<<endl;
  //else cout<<"No specific data/MC year"<<endl;

  for (Long64_t jentry=0; jentry<nentries;jentry++) {
    
    // ==============print number of events done == == == == == == == =
    double progress = 10.0 * jentry / (1.0 * nentries);
    int k = int (progress);
    if (k > decade)
      cout << 10 * k << " %" <<endl;
    decade = k;
    // cout<<"j:"<<jentry<<" fcurrent:"<<fCurrent<<endl;
    // ===============read this entry == == == == == == == == == == == 
    Long64_t ientry = LoadTree(jentry);
    if (ientry < 0) break;
    nb = fChain->GetEntry(jentry);   nbytes += nb;

    //nEvtSurv++;
    h_cutflow->Fill("NEvtsNoWtLeft",1);
    if (ak4_HT > 550) {
            hist_region_1->Fill(jtrip_mass[0]);
        }
  } // loop over entries
  //cout<<"No. of entries survived: "<<nEvtSurv<<endl;
}
