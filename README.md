# MultiJets

Example Ntuplizer:
`python make_flat_jettuple_ak4.py Wjets.txt 0 6`

## Event cuts made in initial sample:
Typical selection rate seems to be ~7.6% (WJetstoQQHT-800toInf)
- len(event.fj_ak4_jetid)<6 
- sum(event.fj_ak4_jetid[:6])<6
- event.fj_ak4_HT<550
- len(gj_index) < 6
  - gj_index lists all jets with qgl > 0.13

## Important Variables:
- triplets:
  - Contains all possible triplet and pair combinations, with different calculated quantities for each combination
  - Takes as an arguement a gj index ranking the quality of the jets in the event
  - Different ones used:
    -trips: uses gql as a gj index
    -jtrips: uses gql as a gj index, with JEC applied
    -prtips: uses pt as a gj index, with JEC applied  
- mds:
  - Find good 6 jets in an event, then take all possible triplet pair combinations
  - For each possible triplet, find the 3 possible invariant mass pairs possible in the 3 jets, m12, m13, m23 (normalized)
  - set mds = Sum(m_ij/2 - 1/sqrt(3))^2
- m63:
  - For each possible triplet out of 6 jets, take the invariant mass of the triplet (normalized)
