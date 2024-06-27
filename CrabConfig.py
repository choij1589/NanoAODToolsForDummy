from CRABClient.UserUtilities import config
from CRABAPI.RawCommand import crabCommand
  
def GetSampleList(file):
  samplelist = file.readlines()
  samplelist = [x.strip() for x in samplelist] 
  samplelist = [x for x in samplelist if x] # Choose lines that are not empty
  samplelist = [x for x in samplelist if not(x.startswith("#"))] # Choose lines that do not start with #

  return samplelist

config = config()
config.General.workArea        = '/data6/Users/yeonjoon/NanoAODToolsForDummy/CMSSW_13_0_10/src/NanoAODToolsForDummy/crab_projects'
config.General.transferOutputs = True
config.General.transferLogs    = False
config.JobType.pluginName = 'Analysis'
config.JobType.psetName   = 'PSet.py'
config.JobType.scriptExe  = 'crab_script.sh'
config.JobType.inputFiles = [
'./branches_in.txt',
'./branches_out.txt',
'./Dumb.py'
#'../../../PhysicsTools/NanoAODTools/scripts/haddnano.py'
]
config.JobType.outputFiles = ['tree.root']
#
config.Data.splitting    = 'FileBased'
config.Data.unitsPerJob = 4
config.Data.publication  = False
config.Data.allowNonValidInputDataset = True
config.JobType.allowUndistributedCMSSW = True
#
# Specify the outLFNDirBase and your storage site
#
#
# JetMET CMS EOS space at CERN
#
#config.Data.outLFNDirBase  = '/u/user/yeonjoon/'
config.Site.storageSite    = 'T2_KR_KISTI'

config.Data.ignoreLocality = True
whitelist_sites=[
'T2_CH_CERN',

]
config.Site.whitelist = whitelist_sites
blacklist_sites=[]
config.Site.blacklist = blacklist_sites

print("Will send crab jobs for the following samples:")
for era in ['2022','2022EE']:
    samplelist = GetSampleList(open("MC_"+era+".txt"))



    for i, dataset in enumerate(samplelist):
        requestName = era + "_" + dataset.split('/')[1]
    
        config.General.requestName = requestName
        config.Data.inputDataset = dataset
        crabCommand('submit', config = config)
        print(f"Submitted {requestName} ({i+1}/{len(samplelist)})")