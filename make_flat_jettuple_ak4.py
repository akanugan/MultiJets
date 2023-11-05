# import ROOT in batch mode
import sys, glob
import ROOT
from ROOT import TH1F, TH1D, TH2D, TFile, TLorentzVector, TChain, TProfile, TTree
from array import array
import argparse
import numpy as np
#import h5py

def tri_mds(trip):
    den=((trip[0]+trip[1]+trip[2]).M()**2)+(trip[0].M()**2)+(trip[1].M()**2)+(trip[2].M()**2)
    m12=((trip[0]+trip[1]).M()**2)/den
    m13=((trip[0]+trip[2]).M()**2)/den
    m23=((trip[2]+trip[1]).M()**2)/den
    d=[m12,m13,m23]
    d.sort()
    r13 = 1/(3**0.5)
    mds=0
    for m in d:
        mds+=((m**0.5)-r13)**2
    tmds = [mds,d[0],d[1],d[2]]
    # print(tmds)
    # print(len(tmds))
    return(tmds)

def mtch_squish(trip):
    mtch=0
    if(trip[0]==1 and trip[1]==1 and trip[2]==1): mtch=1
    elif(trip[0]==2 and trip[1]==2 and trip[2]==2): mtch=2
    elif(trip[0]==-1 and trip[1]==-1 and trip[2]==-1): mtch=-1
    return(mtch)

def flatten(tp_list): #converts triplet pair order
    flat_trip = []
    for obj in tp_list:
        flat_trip.append(obj[0])
        flat_trip.append(obj[1])
    return(flat_trip)


class triplet_pair(object): #Class to calculate the quatities for triplets in pair
    """docstring for triplet"""
    def __init__(self, obj):
        a=obj[0] #Triplet 1
        b=obj[1] #Triplet 2
        self.mass = [(a[0]+a[1]+a[2]).M(),(b[0]+b[1]+b[2]).M()]
        self.vpt = [(a[0]+a[1]+a[2]).Pt(),(b[0]+b[1]+b[2]).Pt()]
        self.spt = [a[0].Pt()+a[1].Pt()+a[2].Pt(),b[0].Pt()+b[1].Pt()+b[2].Pt()]
        self.delta = [a[0].Pt()+a[1].Pt()+a[2].Pt() - (a[0]+a[1]+a[2]).M() , b[0].Pt()+b[1].Pt()+b[2].Pt() - (b[0]+b[1]+b[2]).M()]
        self.eta = [(a[0]+a[1]+a[2]).Eta() , (b[0]+b[1]+b[2]).Eta()]
        self.phi = [(a[0]+a[1]+a[2]).Phi(), (b[0]+b[1]+b[2]).Phi()]
        self.mass_asym = [abs((a[0]+a[1]+a[2]).M() - (b[0]+b[1]+b[2]).M())/((a[0]+a[1]+a[2]).M() + (b[0]+b[1]+b[2]).M()), abs((a[0]+a[1]+a[2]).M() - (b[0]+b[1]+b[2]).M())/((a[0]+a[1]+a[2]).M() + (b[0]+b[1]+b[2]).M())]
        self.delta_eta = [abs((a[0]+a[1]+a[2]).Eta() - (b[0]+b[1]+b[2]).Eta()), abs((a[0]+a[1]+a[2]).Eta() - (b[0]+b[1]+b[2]).Eta())]
        # print(a[0].Pt(),a[1].Pt(),a[2].Pt())
        a_mds = tri_mds(a)
        b_mds = tri_mds(b)
        self.mds = [a_mds[0],b_mds[0]]
        self.dlow = [a_mds[1],b_mds[1]]
        self.dmid = [a_mds[2],b_mds[2]]
        self.dhigh = [a_mds[3],b_mds[3]]


class triplet:
    """docstring for triplet"""
    def __init__(self, jet_pt,jet_eta,jet_phi,jet_m,jet_jec,jet_match,jet_csv,jecm, gji,jet_qgl):
        tl=[]
        # print(jet_pt[:6])
        # print(jet_jec[:6])
        # print(len(jet_pt))
        for i in range(gji[-1]+1): #turn jets into 4 vecs
            # print(i)
            tmp =TLorentzVector()
            if(jecm==0): tmp.SetPtEtaPhiM(jet_pt[i]*1,jet_eta[i],jet_phi[i],jet_m[i]*1)
            else: tmp.SetPtEtaPhiM((jet_pt[i]*jet_jec[i]),jet_eta[i],jet_phi[i],(jet_m[i]*jet_jec[i]))
            tl.append(tmp)
        self.tlv = tl #make it class attribute
        # print(len(tl))
        self.jec = [jet_jec[gji[i]] for i in range(6)] ##make it class attribute
        idx = [[[gji[0], gji[1], gji[2]], [gji[3], gji[4], gji[5]]],
               [[gji[0], gji[1], gji[3]], [gji[2], gji[4], gji[5]]],
               [[gji[0], gji[1], gji[4]], [gji[2], gji[3], gji[5]]],
               [[gji[0], gji[1], gji[5]], [gji[2], gji[3], gji[4]]],
               [[gji[0], gji[2], gji[3]], [gji[1], gji[4], gji[5]]],
               [[gji[0], gji[2], gji[4]], [gji[1], gji[3], gji[5]]],
               [[gji[0], gji[2], gji[5]], [gji[1], gji[3], gji[4]]],
               [[gji[0], gji[3], gji[4]], [gji[1], gji[2], gji[5]]],
               [[gji[0], gji[3], gji[5]], [gji[1], gji[2], gji[4]]],
               [[gji[0], gji[4], gji[5]], [gji[1], gji[2], gji[3]]]]  # all possible triplet and pair combinations

        # print(idx)
        self.ind = idx #index vector
        tj = [] #triplet pair jets
        tjc = [] #triplet pair corrections
        tjm = [] #triplet pair matching
        tpi = [] #triplet indexing
        tpb = []
        tqt = []
        tql = []
        for i,obj in enumerate(idx):
            # print(len(obj),len(obj[0]),len(obj[1]))
            # print('Making triplet pair with [',obj[0][0],obj[0][1],obj[0][2],'], [',obj[1][0],obj[1][1],obj[1][2],']')
            # print( obj[0][0], obj[0][1], obj[0][2], obj[1][0], obj[1][1], obj[1][2] )
            tj.append([ [tl[obj[0][0]], tl[obj[0][1]], tl[obj[0][2]]], [tl[obj[1][0]], tl[obj[1][1]], tl[obj[1][2]]] ])
            tjc.append([ [jet_jec[obj[0][0]], jet_jec[obj[0][1]], jet_jec[obj[0][2]] ], [jet_jec[obj[1][0]], jet_jec[obj[1][1]], jet_jec[obj[1][2]] ] ])
            tjm.append([mtch_squish([jet_match[obj[0][0]],jet_match[obj[0][1]],jet_match[obj[0][2]]]), mtch_squish([jet_match[obj[1][0]],jet_match[obj[1][1]],jet_match[obj[1][2]]])])
            tpb.append([max([jet_csv[obj[0][0]],jet_csv[obj[0][1]],jet_csv[obj[0][2]]]), max([jet_csv[obj[1][0]],jet_csv[obj[1][1]],jet_csv[obj[1][2]]])])
            tqt.append([
                sum([1 if jet_qgl[i] > 0.72 else 0 for i in obj[0]]),
                sum([1 if jet_qgl[i] > 0.72 else 0 for i in obj[1]])
            ])
            tql.append([
                sum([1 if jet_qgl[i] > 0.5 else 0 for i in obj[0]]),
                sum([1 if jet_qgl[i] > 0.5 else 0 for i in obj[1]])
            ])
            tpi.append([i,i])
        self.tp_jets = tj
        self.tp_jec = tjc
        self.tp_match = tjm
        self.tp_ind = tpi
        self.tp_csv = tpb
        self.tp_qgl = tql
        self.tp_qgt = tqt
        # print(tpi)
        # print(tj)
        tps = [triplet_pair(obj) for obj in tj]
        self.tp = tps
        den = 4*((tl[gji[0]]+tl[gji[1]]+tl[gji[2]]+tl[gji[3]]+tl[gji[4]]+tl[gji[5]]).M()**2)
        for i in gji: den+= 6*(tl[i].M()**2)
        self.tp_m63 = [ [((obj.mass[0])**2)/den , ((obj.mass[1])**2)/den] for obj in tps]




we_parms = [['QCD_HT300to500', 5.840092228107049 ],
            ['QCD_HT500to700', 0.5645990685276228 ],
            ['QCD_HT700to1000', 0.15253309779537536 ],
            ['QCD_HT1000to1500', 0.07186338787825997 ],
            ['QCD_HT1500to2000', 0.010317626274751761 ],
            ['QCD_HT2000toInf', 0.004261168431292373 ],
            ['WJetsToQQ_HT400to600', 0.031804503481414066 ],
            ['WJetsToQQ_HT600to800', 0.007793464219281738 ],
            ['WJetsToQQ_HT-800toInf', 0.004318690662087452 ],
            ['ZJetsToQQ_HT400to600', 0.014093617093870954 ],
            ['ZJetsToQQ_HT600to800', 0.0038277115508626313 ],
            ['ZJetsToQQ_HT-800toInf', 0.002387877206580156 ],
            ['TTJets', 0.005344234742928148 ],
            ['DYJets', 0.23695063943283984 ]]



oldargv = sys.argv[:]
sys.argv = [ '-b-' ]
ROOT.gROOT.SetBatch(True)
sys.argv = oldargv
parser = argparse.ArgumentParser()
parser.add_argument("inFile", help="Location of input file/files")
parser.add_argument("isdata", help="data or MC (1 or 0)")
#parser.add_argument("file_num", help="which file to run on")
args = parser.parse_args()

file_list = [line.strip('\n') for line in open(args.inFile).readlines()]
# Ntuples loc
ntup_wjets_loc = '/eos/uscms/store/user/abhijith/WJetsToQQ/WJetsToQQ_HT-800toInf/'
ntup_loc = '/eos/uscms/store/group/lpctrig/abhijith/mc_samples2017/'


#InFile = ntup_wjets_loc + file_list[int(args.file_num)]
#InFile = ntup_loc + file_list[int(args.file_num)]
#InFile = 'WJetsToQQ_HT-800toInf_1.root'
rd = "root://cmseos.fnal.gov//"
redirector = 'root://cmseos.fnal.gov//store/group/lpctrig/abhijith/mc_samples2017/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/Slimmed_Ntuples_QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8_v1/200824_223503/0000/slimmed_ntuple_QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8_v1_1-2.root'
InFile =  file_list[0]
# remove /eos/uscms/
InFile = rd + InFile.replace('/eos/uscms/','')
#InFile = infile

weight=1.0
if(args.isdata==0):
    for p in we_parms:
        if(p[0] in InFile):
            weight = p[1]

# OutFile = 'output2/trip2_'+InFile.split('/')[-1]
#OutFile = 'output2/trip4_'+InFile.split('/')[-1]
OutFile = 'slimmedNtup_'+InFile.split('/')[-1]

#print(InFile,OutFile,args.file_num)
print(InFile,OutFile)

# load FWLite C++ libraries
# ROOT.gSystem.Load("libFWCoreFWLite.so");
# ROOT.gSystem.Load("libDataFormatsFWLite.so");
# ROOT.FWLiteEnabler.enable()

# load FWlite python libraries
# from DataFormats.FWLite import Handle, Events
data_chain=TChain("slimmedntuplizer/events")
#data_files = glob.glob(InFile)
data_files = InFile
#data_files = 'WJetsToQQ_HT-800toInf_1.root'
# for i in data_files:
#     data_chain.Add(i)
data_chain.Add(InFile)

data_chain.SetBranchStatus("*", 0)
####TODO
#### Add masym to tree
#### Add tau for subleading

#gen ak8 and ak11

list_of_sbranches = [
    "Run", "Lumi", "Event", "xscn", "trigger_results", "mds63", "mds6332",
    "jmds63", "jmds6332", "sixpt", "fj_ak4_HT", "loose6j_qgl", "tight6j_qgl",
    "net_tight_qgl", "fj_ak4_num", "trip_num","pmds63", "pmds6332"
]
list_of_jbranches = [
    "fj_ak4_pt", "fj_ak4_eta", "fj_ak4_phi", "fj_ak4_m", "fj_ak4_area",
    "fj_ak4_jec", "fj_ak4_csv", "fj_ak4_jetid", "fj_ak4_match", "fj_ak4_qgl"
]
if(args.isdata==0):
    list_of_jbranches.extend(["fj_ak4_matched_genjet_mass","fj_ak4_matched_genjet_pt","fj_ak4_matched_deltam"])
list_of_tbranches = [
    "trip_mass", "trip_vpt", "trip_spt", "trip_delta", "trip_eta", "trip_phi",
    "trip_masym", "trip_deta", "trip_mds", "trip_dlow", "trip_dmid",
    "trip_dhigh", "trip_match", "trip_tpind", "trip_jind", "trip_csv",
    "trip_m63", "jtrip_mass", "jtrip_vpt", "jtrip_spt", "jtrip_delta",
    "jtrip_eta", "jtrip_phi", "jtrip_masym", "jtrip_deta", "jtrip_mds",
    "jtrip_dlow", "jtrip_dmid", "jtrip_dhigh", "jtrip_match", "jtrip_tpind",
    "jtrip_jind", "jtrip_csv", "jtrip_m63",
    "trip_qgl", "trip_qgt", "jtrip_qgl", "jtrip_qgt",
    "ptrip_mass", "ptrip_vpt", "ptrip_spt", "ptrip_delta","ptrip_eta", "ptrip_phi", "ptrip_masym", "ptrip_deta", "ptrip_mds","ptrip_dlow", "ptrip_dmid", "ptrip_dhigh", "ptrip_match", "ptrip_tpind","ptrip_pind", "ptrip_csv", "ptrip_m63","ptrip_qgl", "ptrip_qgt"
]


for br in (list_of_sbranches+list_of_jbranches):
    if(br != "mds63" and br != "mds6332" and br != "sixpt" and br != "jmds63" and br != "jmds6332" and br != "trip_num" and br != "loose6j_qgl" and br != "tight6j_qgl" and br !="net_tight_qgl"): data_chain.SetBranchStatus(br,1)

jmax=30
tmax=20
data_sarr = [array("f", [0.0]) for obj in range(len(list_of_sbranches)-4)]
data_sarr.extend([array("i", [0]),array("i", [0]),array("f", [0]),array("f", [0])])
data_jarr = [array("f", jmax*[0.0]) for obj in range(len(list_of_jbranches))]
data_tarr = [array("f", tmax*[0.0]) for obj in range(len(list_of_tbranches))]

#reco ak8 and ak11
num_events = data_chain.GetEntries()
print('will process',num_events,'events')

# Book Tree
##AK8 stuff
tree = TTree("events", 'tree with jets')

for i in range(len(list_of_sbranches)-4):
    if(list_of_sbranches[i][:2]=='fj'): tree.Branch(list_of_sbranches[i][3:],data_sarr[i],list_of_sbranches[i][3:]+"/F")
    else : tree.Branch(list_of_sbranches[i],data_sarr[i],list_of_sbranches[i]+"/F")

tree.Branch(list_of_sbranches[-4][3:],data_sarr[-4],list_of_sbranches[-4][3:]+"/I")
tree.Branch(list_of_sbranches[-3],data_sarr[-3],list_of_sbranches[-3]+"/I")
tree.Branch(list_of_sbranches[-2],data_sarr[-2],list_of_sbranches[-2]+"/F")
tree.Branch(list_of_sbranches[-1],data_sarr[-1],list_of_sbranches[-1]+"/F")

for i in range(len(list_of_jbranches)):
    tree.Branch(list_of_jbranches[i][3:],data_jarr[i],list_of_jbranches[i][3:]+"[ak4_num]/F")

for i in range(len(list_of_tbranches)):
    tree.Branch(list_of_tbranches[i],data_tarr[i],list_of_tbranches[i]+"[trip_num]/F")


#done booking the tree

cut_flow_hist = TH1F("cut_flow_hist","cut_flow_hist",5,0,5)
count=0
for event in data_chain:
    count+=1
    cut_flow_hist.Fill(0)
    if(count%1000==0 or count == num_events): print("wrote event :",count,";",100*count/num_events,"%  done ")
    if(len(event.fj_ak4_jetid)<6): continue
    cut_flow_hist.Fill(1)
    if(sum(event.fj_ak4_jetid[:6])<6): continue
    cut_flow_hist.Fill(2)
    if(event.fj_ak4_HT<550): continue
    cut_flow_hist.Fill(3)
    gj_index = []
    gj_qgl = []
    for i, qgl in enumerate(event.fj_ak4_qgl):
        if (qgl > 0.13):
            gj_index.append(i)
            gj_qgl.append(qgl)
    if (len(gj_index) < 6): continue
    cut_flow_hist.Fill(4)
    n=min(len(event.fj_ak4_pt),30)
    # print(gj_index,gj_qgl)

    #Repeat with JECs
    jtrips = triplet(event.fj_ak4_pt, event.fj_ak4_eta, event.fj_ak4_phi,
                     event.fj_ak4_m, event.fj_ak4_jec, event.fj_ak4_match,
                     event.fj_ak4_csv, 1, gj_index, event.fj_ak4_qgl)
    jtrip_mass = flatten([obj.mass for obj in jtrips.tp])
    jtrip_vpt = flatten([obj.vpt for obj in jtrips.tp])
    jtrip_spt = flatten([obj.spt for obj in jtrips.tp])
    jtrip_delta = flatten([obj.delta for obj in jtrips.tp])
    jtrip_eta = flatten([obj.eta for obj in jtrips.tp])
    jtrip_phi = flatten([obj.phi for obj in jtrips.tp])
    jtrip_masym = flatten([obj.mass_asym for obj in jtrips.tp])
    jtrip_deta = flatten([obj.delta_eta for obj in jtrips.tp])
    jtrip_mds = flatten([obj.mds for obj in jtrips.tp])
    jtrip_dlow = flatten([obj.dlow for obj in jtrips.tp])
    jtrip_dmid = flatten([obj.dmid for obj in jtrips.tp])
    jtrip_dhigh = flatten([obj.dhigh for obj in jtrips.tp])
    jtrip_match = flatten(jtrips.tp_match)
    jtrip_tpind = flatten(jtrips.tp_ind)
    jtrip_jind = [((obj[0]+1)*100)+((obj[1]+1)*10)+(obj[2]+1) for obj in flatten(jtrips.ind)]
    jtrip_csv = flatten(jtrips.tp_csv)
    jtrip_m63 = flatten(jtrips.tp_m63)

    #Do triplet cals
    trips = triplet(event.fj_ak4_pt, event.fj_ak4_eta, event.fj_ak4_phi,
                    event.fj_ak4_m, event.fj_ak4_jec, event.fj_ak4_match,
                    event.fj_ak4_csv, 0, gj_index, event.fj_ak4_qgl)
    trip_mass = flatten([obj.mass for obj in trips.tp])
    trip_vpt = flatten([obj.vpt for obj in trips.tp])
    trip_spt = flatten([obj.spt for obj in trips.tp])
    trip_delta = flatten([obj.delta for obj in trips.tp])
    trip_eta = flatten([obj.eta for obj in trips.tp])
    trip_phi = flatten([obj.phi for obj in trips.tp])
    trip_masym = flatten([obj.mass_asym for obj in trips.tp])
    trip_deta = flatten([obj.delta_eta for obj in trips.tp])
    trip_mds = flatten([obj.mds for obj in trips.tp])
    trip_dlow = flatten([obj.dlow for obj in trips.tp])
    trip_dmid = flatten([obj.dmid for obj in trips.tp])
    trip_dhigh = flatten([obj.dhigh for obj in trips.tp])
    trip_match = flatten(trips.tp_match)
    trip_tpind = flatten(trips.tp_ind)
    trip_jind = [((obj[0]+1)*100)+((obj[1]+1)*10)+(obj[2]+1) for obj in flatten(trips.ind)]
    trip_csv = flatten(trips.tp_csv)
    trip_m63 = flatten(trips.tp_m63)

    #qgl stuff
    jtrip_qgl = flatten(jtrips.tp_qgl)
    jtrip_qgt = flatten(jtrips.tp_qgt)

    trip_qgl = flatten(trips.tp_qgl)
    trip_qgt = flatten(trips.tp_qgt)

    #Repeat with JECs
    pt_index =[0,1,2,3,4,5]
    ptrips = triplet(event.fj_ak4_pt, event.fj_ak4_eta, event.fj_ak4_phi,
                     event.fj_ak4_m, event.fj_ak4_jec, event.fj_ak4_match,
                     event.fj_ak4_csv, 1, pt_index, event.fj_ak4_qgl)
    ptrip_mass = flatten([obj.mass for obj in ptrips.tp])
    ptrip_vpt = flatten([obj.vpt for obj in ptrips.tp])
    ptrip_spt = flatten([obj.spt for obj in ptrips.tp])
    ptrip_delta = flatten([obj.delta for obj in ptrips.tp])
    ptrip_eta = flatten([obj.eta for obj in ptrips.tp])
    ptrip_phi = flatten([obj.phi for obj in ptrips.tp])
    ptrip_masym = flatten([obj.mass_asym for obj in ptrips.tp])
    ptrip_deta = flatten([obj.delta_eta for obj in ptrips.tp])
    ptrip_mds = flatten([obj.mds for obj in ptrips.tp])
    ptrip_dlow = flatten([obj.dlow for obj in ptrips.tp])
    ptrip_dmid = flatten([obj.dmid for obj in ptrips.tp])
    ptrip_dhigh = flatten([obj.dhigh for obj in ptrips.tp])
    ptrip_match = flatten(ptrips.tp_match)
    ptrip_tpind = flatten(ptrips.tp_ind)
    ptrip_jind = [((obj[0]+1)*100)+((obj[1]+1)*10)+(obj[2]+1) for obj in flatten(ptrips.ind)]
    ptrip_csv = flatten(ptrips.tp_csv)
    ptrip_m63 = flatten(ptrips.tp_m63)
    ptrip_qgl = flatten(ptrips.tp_qgl)
    ptrip_qgt = flatten(ptrips.tp_qgt)



    r120 = 1/(20**0.5)

    mds63=0
    for m in trip_m63:
        mds63+=((m**0.5)-r120)**2
    mds6332=0
    for i in range(20):
        mds6332+=(((trip_m63[i]+trip_mds[i])**0.5)-r120)**2

    jmds63=0
    for m in jtrip_m63:
        jmds63+=((m**0.5)-r120)**2
    jmds6332=0
    for i in range(20):
        jmds6332+=(((jtrip_m63[i]+jtrip_mds[i])**0.5)-r120)**2
    
    pmds63=0
    for m in ptrip_m63:
        pmds63+=((m**0.5)-r120)**2
    pmds6332=0
    for i in range(20):
        pmds6332+=(((ptrip_m63[i]+ptrip_mds[i])**0.5)-r120)**2

    lqgl = 0
    for i in range(n):
        if(event.fj_ak4_qgl[i]<0.5): break
        else: lqgl+=1

    tqgl = 0
    for i in range(n):
        if(event.fj_ak4_qgl[i]<0.72): break
        else: tqgl+=1

    nqgl = 0
    for i in range(n):
        if(event.fj_ak4_qgl[i]>0.72): nqgl+=1

    data_sarr[0][0]=event.Run
    data_sarr[1][0]=event.Lumi
    data_sarr[2][0]=event.Event
    data_sarr[3][0]=weight
    data_sarr[4][0]=1
    data_sarr[5][0]=mds63
    data_sarr[6][0]=mds6332
    data_sarr[7][0]=jmds63
    data_sarr[8][0]=jmds6332
    data_sarr[9][0]=event.fj_ak4_pt[5]
    data_sarr[10][0]=event.fj_ak4_HT
    data_sarr[11][0] = lqgl
    data_sarr[12][0] = tqgl
    data_sarr[13][0] = nqgl
    data_sarr[14][0]=min(len(event.fj_ak4_pt),30)
    data_sarr[15][0]=20
    data_sarr[16][0]=pmds63
    data_sarr[17][0]=pmds6332

    #print(count, '#event')
    #for obj in data_sarr:
    # print(obj[0],)
    # print('done init')
    for i in range(n):
        data_jarr[0][i]=event.fj_ak4_pt[i]
        data_jarr[1][i]=event.fj_ak4_eta[i]
        data_jarr[2][i]=event.fj_ak4_phi[i]
        data_jarr[3][i]=event.fj_ak4_m[i]
        data_jarr[4][i]=event.fj_ak4_area[i]
        data_jarr[5][i]=event.fj_ak4_jec[i]
        data_jarr[6][i]=event.fj_ak4_csv[i]
        data_jarr[7][i]=event.fj_ak4_jetid[i]
        data_jarr[8][i]=event.fj_ak4_match[i]
        data_jarr[9][i]=event.fj_ak4_qgl[i]
        if(args.isdata==0):  
            data_jarr[10][i]=event.fj_ak4_matched_genjet_mass[i]
            data_jarr[11][i]=event.fj_ak4_matched_genjet_pt[i]
            data_jarr[12][i]=event.fj_ak4_matched_deltam[i]


    for i in range(20):
        data_tarr[0][i]=trip_mass[i]
        data_tarr[1][i]=trip_vpt[i]
        data_tarr[2][i]=trip_spt[i]
        data_tarr[3][i]=trip_delta[i]
        data_tarr[4][i]=trip_eta[i]
        data_tarr[5][i]=trip_phi[i]
        data_tarr[6][i]=trip_masym[i]
        data_tarr[7][i]=trip_deta[i]
        data_tarr[8][i]=trip_mds[i]
        data_tarr[9][i]=trip_dlow[i]
        data_tarr[10][i]=trip_dmid[i]
        data_tarr[11][i]=trip_dhigh[i]
        data_tarr[12][i]=trip_match[i]
        data_tarr[13][i]=trip_tpind[i]
        data_tarr[14][i]=trip_jind[i]
        data_tarr[15][i]=trip_csv[i]
        data_tarr[16][i]=trip_m63[i]

        data_tarr[17][i]=jtrip_mass[i]
        data_tarr[18][i]=jtrip_vpt[i]
        data_tarr[19][i]=jtrip_spt[i]
        data_tarr[20][i]=jtrip_delta[i]
        data_tarr[21][i]=jtrip_eta[i]
        data_tarr[22][i]=jtrip_phi[i]
        data_tarr[23][i]=jtrip_masym[i]
        data_tarr[24][i]=jtrip_deta[i]
        data_tarr[25][i]=jtrip_mds[i]
        data_tarr[26][i]=jtrip_dlow[i]
        data_tarr[27][i]=jtrip_dmid[i]
        data_tarr[28][i]=jtrip_dhigh[i]
        data_tarr[29][i]=jtrip_match[i]
        data_tarr[30][i]=jtrip_tpind[i]
        data_tarr[31][i]=jtrip_jind[i]
        data_tarr[32][i]=jtrip_csv[i]
        data_tarr[33][i]=jtrip_m63[i]

        #qgl stuff
        data_tarr[34][i] = trip_qgl[i]
        data_tarr[35][i] = trip_qgt[i]
        data_tarr[36][i] = jtrip_qgl[i]
        data_tarr[37][i] = jtrip_qgt[i]

        data_tarr[38][i] = ptrip_mass[i]
        data_tarr[39][i] = ptrip_vpt[i]
        data_tarr[40][i] = ptrip_spt[i]
        data_tarr[41][i] = ptrip_delta[i]
        data_tarr[42][i] = ptrip_eta[i]
        data_tarr[43][i] = ptrip_phi[i]
        data_tarr[44][i] = ptrip_masym[i]
        data_tarr[45][i] = ptrip_deta[i]
        data_tarr[46][i] = ptrip_mds[i]
        data_tarr[47][i] = ptrip_dlow[i]
        data_tarr[48][i] = ptrip_dmid[i]
        data_tarr[49][i] = ptrip_dhigh[i]
        data_tarr[50][i] = ptrip_match[i]
        data_tarr[51][i] = ptrip_tpind[i]
        data_tarr[52][i] = ptrip_jind[i]
        data_tarr[53][i] = ptrip_csv[i]
        data_tarr[54][i] = ptrip_m63[i]
        data_tarr[55][i] = ptrip_qgl[i]
        data_tarr[56][i] = ptrip_qgt[i]

    tree.Fill()


outfile = TFile(OutFile, "recreate")
cut_flow_hist.Write()
tree.Write()
outfile.Write()
outfile.Close()

