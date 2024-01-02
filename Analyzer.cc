#define Analyzer_cxx
#include "Analyzer.h"
#include <TH1.h>
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TLorentzVector.h>
#include <iostream>
#include <vector>
#include <cstring>
#include <string>
#include <map>
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
  ana.CopyCutFlow();
  ana.EventLoop(data,inputFileList);
  return 0;
}

void Analyzer::EventLoop(const char *data,const char *inputFileList) {
  if (fChain == 0) return;

  //Here I define x-secs for weighting purposes. If there's a better spot to 
  //define this map it can be moved
  // map<string,float> x_sections;
  // x_sections["QCD_HT300to500"] = 0;
  // x_sections["QCD_HT500to700"] = 29370;
  // x_sections["QCD_HT700to1000"] = 6524;
  // x_sections["QCD_HT1000to1500"] = 1064;
  // x_sections["QCD_HT1500to2000"] =121.5;
  // x_sections["QCD_HT2000toInf"] = 25.42;
  
  

  Long64_t nentries = fChain->GetEntries();
  cout << "nentries " << nentries << endl;
  cout << "Analyzing dataset " << data << " " << endl;

  TString s_data=data;
  Long64_t nbytes = 0, nb = 0;
  int decade = 0;
  //if(dataRun>0) cout<<"Processing it as "<<dataRun<<" data"<<endl;
  //else if(dataRun<0) cout<<"Processing it as "<<abs(dataRun)<<" MC"<<endl;
  //else cout<<"No specific data/MC year"<<endl;

  for (Long64_t jentry=0; jentry<nentries;jentry++) {
    
    
    // TChain *name_finder = (TChain*) fChain;
    // string na = name_finder->GetFile()->GetName();
    // auto start = na.find("QCD_HT");
    // auto end = na.find("_", start + 5);
    // string target = na.substr(start,end - start);
    // string name = na.substr(start);
    // float x_section = x_sections[target];
    // float pre_cut_events = name_finder->GetFile()->Get<TH1>("cut_flow_hist")->GetBinContent(1);
    // float weight = x_section / pre_cut_events;


    // ==============print number of events done == == == == == == == =
    double progress = 10.0 * jentry / (1.0 * nentries);
    int k = int (progress);
    if (k > decade){
      cout << 10 * k << " %" <<endl;
    }
    decade = k;
    // cout<<"j:"<<jentry<<" fcurrent:"<<fCurrent<<endl;
    // ===============read this entry == == == == == == == == == == == 
    Long64_t ientry = LoadTree(jentry);

    
    
    //float weight = x_section / pre_cut_events;
    
    if (ientry < 0) break;
    nb = fChain->GetEntry(jentry);   nbytes += nb;

    //nEvtSurv++;
    h_cutflow->Fill("NEvtsNoWtLeft",1);
    ht_plot->Fill(ak4_HT,1);
    float lowest_mass_asym = jtrip_masym[0];
    int lowest_mass_asym_index = 0;
    float lowest_delta= jtrip_delta[0];
    int lowest_delta_index = 0;
    if (ak4_HT > 550) {
            for ( int i = 0; i < 20; i++){
              hist_region_1->Fill(jtrip_mass[i],1);
              if (jtrip_masym[i] <= lowest_mass_asym)
              {
                lowest_mass_asym_index = i;
                lowest_mass_asym = jtrip_masym[i];
              }
              if (jtrip_delta[i] <= lowest_delta)
              {
                lowest_delta_index = i;
                lowest_delta = jtrip_delta[i];
              }
              //if (sixpt>50 && jmds6332<1.25 && jtrip_masym[i] <0.175 && jtrip_delta[i]>180 && jtrip_mds[i]<0.175 && jtrip_qgl[i]>1 && jtrip_qgt[i]>0){
                //hist_region_3->Fill(jtrip_mass[i],1);
              //}
            }
        }
    //this is to get to the lower even number
    //for example if the index is 15, we want to be at 14
    //but if its at 14, we want to stay at 14
    lowest_mass_asym_index = lowest_mass_asym_index/2;
    lowest_mass_asym_index = 2*lowest_mass_asym_index;
    if (jtrip_mass[lowest_mass_asym_index] > jtrip_mass[lowest_mass_asym_index + 1]){
      hist_region_2->Fill(jtrip_mass[lowest_mass_asym_index],1);
      h_b_jtrip_masym->Fill(jtrip_masym[lowest_mass_asym_index],1);
      h_b_jtrip_delta->Fill(jtrip_delta[lowest_mass_asym_index],1);
    }
    else {
      hist_region_2->Fill(jtrip_mass[lowest_mass_asym_index + 1],1);
      h_b_jtrip_masym->Fill(jtrip_masym[lowest_mass_asym_index + 1],1);
      h_b_jtrip_delta->Fill(jtrip_delta[lowest_mass_asym_index],1);
    }


    

    hist_region_3->Fill(ptrip_mass[lowest_delta_index],1);
    
  } // loop over entries
  //cout<<"No. of entries survived: "<<nEvtSurv<<endl;
}
