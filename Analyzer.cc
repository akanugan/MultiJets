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



    vector<float> region_val;
    vector<int> region_index;

    region_val.push_back(jtrip_masym[0]);
    region_index.push_back(0);
    
    region_val.push_back(jtrip_delta[0]);
    region_index.push_back(0);

    region_val.push_back(abs(abs(jtrip_phi[1] - jtrip_phi[0]) - 3.1415));
    region_index.push_back(0);
    
    region_val.push_back(abs(jtrip_mds[0]));
    region_index.push_back(0);

    region_val.push_back(abs(jtrip_qgl[0]));
    region_index.push_back(0);


    if (ak4_HT > 550) {
            for ( int i = 0; i < 20; i++){

              
              hist_regions.at(0)->Fill(jtrip_mass[i],1);
              hist_variables.at(0).at(0)->Fill(jtrip_masym[i],1);
              hist_variables.at(1).at(0)->Fill(jtrip_delta[i],1);
              hist_variables.at(3).at(0)->Fill(jtrip_mds[i],1);
              hist_variables.at(4).at(0)->Fill(jtrip_qgl[i],1);
              
              

              if (jtrip_masym[i] < region_val.at(0))
              {
                region_index.at(0) = i;
                region_val.at(0) = jtrip_masym[i];
              }

              if (jtrip_delta[i] > region_val.at(1))
              {
                region_index.at(1) = i;
                region_val.at(1) = jtrip_delta[i];
              }

              if (i % 2 == 0)
              {
                hist_variables.at(2).at(0)->Fill(abs(abs(jtrip_phi[i+1] - jtrip_phi[i]) - 3.1415),1);
                float phi_d = abs(abs(jtrip_phi[i+1] - jtrip_phi[i]) - 3.1415);
                if(phi_d < region_val.at(2))
                {
                  region_index.at(2) = i;
                  region_val.at(2) = phi_d;
                }
              }

              if (jtrip_mds[i] < region_val.at(3)){
                region_index.at(3) = i;
                region_val.at(3) = jtrip_mds[i];
              }

              if (jtrip_qgl[i] > region_val.at(4)){
                region_index.at(4) = i;
                region_val.at(4) = jtrip_qgl[i];
              }
              else if(jtrip_qgl[i] == region_val.at(4) && jtrip_vpt[i] > jtrip_vpt[region_index.at(4)])
              {
                region_index.at(4) = i;
                region_val.at(4) = jtrip_qgl[i];
              }
              //if (sixpt>50 && jmds6332<1.25 && jtrip_masym[i] <0.175 && jtrip_delta[i]>180 && jtrip_mds[i]<0.175 && jtrip_qgl[i]>1 && jtrip_qgt[i]>0){
                //hist_region_3->Fill(jtrip_mass[i],1);
              //}
            }
    }

    


    //this is to get to the lower even number
    //for example if the index is 15, we want to be at 14
    //but if its at 14, we want to stay at 14

    vector<float> region_i_dphi;
    
    for(int i =0; i < variables.size(); i++){
      region_index.at(i) = region_index.at(i)/2;
      region_index.at(i) = 2*region_index.at(i);
      region_i_dphi.push_back( abs(abs(jtrip_phi[region_index.at(i)+1] - jtrip_phi[region_index.at(i)]) - 3.1415));
      hist_variables.at(2).at(i+1)->Fill(region_i_dphi.at(i),1);

      if (jtrip_mass[region_index.at(i)] < jtrip_mass[region_index.at(i) + 1]){
        region_index.at(i) = region_index.at(i) + 1;
      }
      
      hist_regions.at(i+1)->Fill(jtrip_mass[region_index.at(i)],1);
      hist_variables.at(0).at(i+1)->Fill(jtrip_masym[region_index.at(i)],1);
      hist_variables.at(1).at(i+1)->Fill(jtrip_delta[region_index.at(i)],1);
      hist_variables.at(3).at(i+1)->Fill(jtrip_mds[region_index.at(i)],1);
      hist_variables.at(4).at(i+1)->Fill(jtrip_qgl[region_index.at(i)],1);
    }


    
    cross_variables.at(0).at(1)->Fill(jtrip_masym[region_index.at(0)],jtrip_delta[region_index.at(0)]);
    cross_variables.at(0).at(2)->Fill(jtrip_masym[region_index.at(0)],region_i_dphi.at(0));
    cross_variables.at(0).at(3)->Fill(jtrip_masym[region_index.at(0)],jtrip_mds[region_index.at(0)]);
    cross_variables.at(0).at(4)->Fill(jtrip_masym[region_index.at(0)],jtrip_qgl[region_index.at(0)]);

    cross_variables.at(1).at(0)->Fill(jtrip_delta[region_index.at(1)],jtrip_masym[region_index.at(1)]);
    cross_variables.at(1).at(2)->Fill(jtrip_delta[region_index.at(1)],region_i_dphi.at(1));
    cross_variables.at(1).at(3)->Fill(jtrip_delta[region_index.at(1)],jtrip_mds[region_index.at(1)]);
    cross_variables.at(1).at(4)->Fill(jtrip_delta[region_index.at(1)],jtrip_qgl[region_index.at(1)]);

    cross_variables.at(2).at(0)->Fill(region_i_dphi.at(2),jtrip_masym[region_index.at(2)]);
    cross_variables.at(2).at(1)->Fill(region_i_dphi.at(2),jtrip_delta[region_index.at(2)]);
    cross_variables.at(2).at(3)->Fill(region_i_dphi.at(2),jtrip_mds[region_index.at(2)]);
    cross_variables.at(2).at(4)->Fill(region_i_dphi.at(2),jtrip_qgl[region_index.at(2)]);

    cross_variables.at(3).at(0)->Fill(jtrip_mds[region_index.at(3)],jtrip_masym[region_index.at(3)]);
    cross_variables.at(3).at(1)->Fill(jtrip_mds[region_index.at(3)],jtrip_delta[region_index.at(3)]);
    cross_variables.at(3).at(2)->Fill(jtrip_mds[region_index.at(3)],region_i_dphi.at(3));
    cross_variables.at(3).at(4)->Fill(jtrip_mds[region_index.at(3)],jtrip_qgl[region_index.at(3)]);

    cross_variables.at(4).at(0)->Fill(jtrip_qgl[region_index.at(4)],jtrip_masym[region_index.at(4)]);
    cross_variables.at(4).at(1)->Fill(jtrip_qgl[region_index.at(4)],jtrip_delta[region_index.at(4)]);
    cross_variables.at(4).at(2)->Fill(jtrip_qgl[region_index.at(4)],region_i_dphi.at(4));
    cross_variables.at(4).at(3)->Fill(jtrip_qgl[region_index.at(4)],jtrip_mds[region_index.at(4)]);
    
    
  } // loop over entries
  //cout<<"No. of entries survived: "<<nEvtSurv<<endl;
}
