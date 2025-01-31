import os
import argparse
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *

print('HeLlO We aRE GoINg tO MeRGE FiLeS')
from PhysicsTools.NanoAODTools.postprocessing.utils.crabhelper import inputFiles, runsAndLumis

#print('inputFiles()')
#print(inputFiles())
parser = argparse.ArgumentParser("")
parser.add_argument("--isData", default=0)
parser.add_argument("--jobNum", default=1)
parser.add_argument("--era", default='', type=str)
args = parser.parse_args()
isData = int(args.isData)
era = str(args.era)

jsonInput = None
if era == '2018':
    jsonInput = "Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.json"
elif era == '2017':
    jsonInput = "Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.json"
elif era == '2016postVFP':
    jsonInput = "Cert_271036-284044_13TeV_Legacy2016_Collisions16.json"
elif era == '2016preVFP':
    jsonInput = "Cert_271036-284044_13TeV_Legacy2016_Collisions16.json"
elif era == '2022' or era == '2022EE':
    jsonInput = "Cert_Collisions2022_355100_362760_Golden.json"
elif era == '2023' or era == '2023BPix':
    jsonInput = "Cert_Collisions2023_366442_370790_Golden.json"
else:
    print(f'era {era} not found, exiting')
    exit()

print(f'era: {era}, isData: {isData}, jsonInput: {jsonInput}')

#CMSXROOTD="root://cms-xrd-global.cern.ch//"
#files = ["/store/mc/RunIISummer20UL16NanoAODAPVv9/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/280000/E9B9F84B-B094-504F-967E-CC85267C7F21.root"]
#files = [CMSXROOTD+file for file in files]

p=PostProcessor(
  ".",
  inputFiles(),
  branchsel="branches_in.txt",
  outputbranchsel="branches_out.txt",
  fwkJobReport=True,
  provenance=True,
  prefetch = False,
  jsonInput=jsonInput if isData else None,
)
p.run()
print('Done')
