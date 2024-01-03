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

  Long64_t nentries = fChain->GetEntries();
  cout << "nentries " << nentries << endl;
  cout << "Analyzing dataset " << data << " " << endl;

  TString s_data=data;
  Long64_t nbytes = 0, nb = 0;
  int decade = 0;

  for (Long64_t jentry=0; jentry<nentries;jentry++) {
    
    


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



    float region_2_val = jtrip_masym[0];
    int region_2_index = 0;
    
    float region_3_val = abs(jtrip_delta[0]);
    int region_3_index = 0;

    float region_4_val = abs(abs(jtrip_phi[1] - jtrip_phi[0]) - 3.1415);
    int region_4_index = 0;
    


    if (ak4_HT > 550) {
            for ( int i = 0; i < 20; i++){

              hist_region_1->Fill(jtrip_mass[i],1);
              hist_variables.at(0).at(0)->Fill(jtrip_masym[i],1);
              hist_variables.at(1).at(0)->Fill(jtrip_delta[i],1);
              

              if (jtrip_masym[i] < region_2_val)
              {
                region_2_index = i;
                region_2_val = jtrip_masym[i];
              }

              if (abs(jtrip_delta[i]) < region_3_val)
              {
                region_3_index = i;
                region_3_val = abs(jtrip_delta[i]);
              }

              if (i % 2 == 0)
              {
                hist_variables.at(2).at(0)->Fill(abs(abs(jtrip_phi[i+1] - jtrip_phi[i]) - 3.1415),1);
                float phi_d = abs(abs(jtrip_phi[i+1] - jtrip_phi[i]) - 3.1415);
                if(phi_d < region_4_val)
                {
                  region_4_index = i;
                  region_4_val = phi_d;
                }

              }
              //if (sixpt>50 && jmds6332<1.25 && jtrip_masym[i] <0.175 && jtrip_delta[i]>180 && jtrip_mds[i]<0.175 && jtrip_qgl[i]>1 && jtrip_qgt[i]>0){
                //hist_region_3->Fill(jtrip_mass[i],1);
              //}
            }
    }



    //this is to get to the lower even number
    //for example if the index is 15, we want to be at 14
    //but if its at 14, we want to stay at 14
    region_2_index = region_2_index/2;
    region_2_index = 2*region_2_index;
    float region_2_dphi = abs(abs(jtrip_phi[region_2_index+1] - jtrip_phi[region_2_index]) - 3.1415);
    hist_variables.at(2).at(1)->Fill(region_2_dphi,1);
    if (jtrip_mass[region_2_index] < jtrip_mass[region_2_index + 1]){
      region_2_index = region_2_index + 1;
    }
    hist_region_2->Fill(jtrip_mass[region_2_index],1);
    hist_variables.at(0).at(1)->Fill(jtrip_masym[region_2_index],1);
    hist_variables.at(1).at(1)->Fill(jtrip_delta[region_2_index],1);

    cross_variables.at(0).at(1)->Fill(jtrip_masym[region_2_index],jtrip_delta[region_2_index]);
    cross_variables.at(0).at(2)->Fill(jtrip_masym[region_2_index],region_2_dphi);


    region_3_index = region_3_index/2;
    region_3_index = 2*region_3_index;
    float region_3_dphi = abs(abs(jtrip_phi[region_3_index+1] - jtrip_phi[region_3_index]) - 3.1415);
    hist_variables.at(2).at(2)->Fill(region_3_dphi,1);
    if (jtrip_mass[region_3_index] < jtrip_mass[region_3_index + 1]){
      region_3_index = region_3_index + 1;
    }
    hist_region_3->Fill(jtrip_mass[region_3_index],1);
    hist_variables.at(0).at(2)->Fill(jtrip_masym[region_3_index],1);
    hist_variables.at(1).at(2)->Fill(jtrip_delta[region_3_index],1);

    cross_variables.at(1).at(0)->Fill(jtrip_delta[region_3_index],jtrip_masym[region_3_index]);
    cross_variables.at(1).at(2)->Fill(jtrip_delta[region_3_index],region_3_dphi);


    region_4_index = region_4_index/2;
    region_4_index = 2*region_4_index;
    float region_4_dphi = abs(abs(jtrip_phi[region_4_index+1] - jtrip_phi[region_4_index]) - 3.1415);
    hist_variables.at(2).at(3)->Fill(region_4_dphi,1);
    if (jtrip_mass[region_4_index] > jtrip_mass[region_4_index + 1]){
      region_4_index = region_4_index + 1;
    }
    hist_region_4->Fill(jtrip_mass[region_4_index],1);
    hist_variables.at(0).at(3)->Fill(jtrip_masym[region_4_index],1);
    hist_variables.at(1).at(3)->Fill(jtrip_delta[region_4_index],1);

    cross_variables.at(2).at(0)->Fill(region_4_dphi,jtrip_masym[region_4_index]);
    cross_variables.at(2).at(1)->Fill(region_4_dphi,jtrip_delta[region_4_index]);

    
  } // loop over entries
  //cout<<"No. of entries survived: "<<nEvtSurv<<endl;
}
