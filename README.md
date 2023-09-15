# MultiJets

Example Ntuplizer:
`python make_flat_jettuple_ak4.py Wjets.txt 0 6`

## Event cuts made:
Typical selection rate seems to be ~7.6% (WJetstoQQHT-800toInf)
- len(event.fj_ak4_jetid)<6 
- sum(event.fj_ak4_jetid[:6])<6
- event.fj_ak4_HT<550
- len(gj_index) < 6
  - gj_index lists all jets with qgl > 0.13

## Important Variables:
- 
- 
