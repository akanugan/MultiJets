eosls /store/user/abhijith/run2_multijet/ntuples/ | grep gl700 > filelist/sig_gl70sed 's/^/root:\/\/cmseos.fnal.gov\/\/store\/user\/abhijith\/run2_multijet\/ntuples\//; s/$//' filelist/sig_gl700.txt > sig_gl700.txt
sed 's/^/root:\/\/cmseos.fnal.gov\/\/store\/user\/abhijith\/run2_multijet\/ntuples\//; s/$//' filelist/sig_gl700.txt > sig_gl700.txt
mkdir temp_signal
cd temp_signal/
cd ..
xrdcp $(cat sig_gl700.txt) temp_signal/
hadd full_ntuples/trip4_gl700.root temp_signal/*
rm -r temp_signal/
