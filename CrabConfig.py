from CRABClient.UserUtilities import config
from CRABAPI.RawCommand import crabCommand
import re
import os

def GetSampleList(file):
  samplelist = file.readlines()
  samplelist = [x.strip() for x in samplelist] 
  samplelist = [x for x in samplelist if x] # Choose lines that are not empty
  samplelist = [x for x in samplelist if not(x.startswith("#"))] # Choose lines that do not start with #
  return samplelist

config = config()


def getUnitsPerJob(datasetName, evtPerJob=200000):
  query = os.popen(f"/cvmfs/cms.cern.ch/common/dasgoclient --query 'summary dataset={datasetName}'").read()
  #sample output = [{"file_size":309022244066,"max_ldate":1628354012,"median_cdate":null,"median_ldate":1627591054,"nblocks":39,"nevents":145020000,"nfiles":155,"nlumis":145020,"num_block":39,"num_event":145020000,"num_file":155,"num_lumi":145020}]
  num_lumi = int(re.search(r'"num_lumi":(\d+)', query).group(1))
  num_event = int(re.search(r'"num_event":(\d+)', query).group(1))
  eventPerLumi = num_event/num_lumi
  #target is roughly 200000 events per job
  unitsPerJob = int(evtPerJob/eventPerLumi)
  if unitsPerJob == 0: unitsPerJob = 1
  print(f'query: {query}')
  print(f'num_lumi: {num_lumi}, num_event: {num_event}, eventPerLumi: {eventPerLumi}, unitsPerJob: {unitsPerJob}')
  return unitsPerJob


config.General.workArea        = 'crab_projects_0105'
config.General.transferOutputs = True
config.General.transferLogs    = False
config.JobType.pluginName = 'Analysis'
config.JobType.psetName   = 'PSet.py'
config.JobType.scriptExe  = 'crab_script.sh'
config.Data.ignoreLocality = False

config.JobType.inputFiles = [
'./branches_in.txt',
'./branches_out.txt',
'./Dumb.py',
#'../scripts/haddnano.py',
'./Cert_Collisions2022_355100_362760_Golden.json',
'./Cert_271036-284044_13TeV_Legacy2016_Collisions16.json',
'./Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.json',
'./Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.json',
'./Cert_Collisions2023_366442_370790_Golden.json',
#'../../../PhysicsTools/NanoAODTools/scripts/haddnano.py'mamba
]
config.JobType.outputFiles = ['tree.root']
#
config.Data.splitting    = 'LumiBased'
#config.Data.splitting    = 'FileBased'
config.Data.unitsPerJob = 30
config.Data.publication  = False
config.Data.inputDBS = 'global'
config.Data.allowNonValidInputDataset = False
config.JobType.allowUndistributedCMSSW = False
config.Data.outLFNDirBase = '/store/user/yeonjoon/SKNano_0105/'
#config.Site.storageSite    = 'T2_KR_KISTI'
config.Site.storageSite    = 'T3_KR_KNU'

whitelist_sites=[


]
config.Site.whitelist = whitelist_sites
blacklist_sites=[]
config.Site.blacklist = blacklist_sites


for era in ['2023']:
    
    samplelist = GetSampleList(open("DATA_"+era+".txt"))
    for i, dataset in enumerate(samplelist):
        continue
        if dataset.startswith("#"): continue
        config.JobType.scriptArgs = ['isData=1']
        requestName = era + "_" + dataset.split('/')[1]
        e = ''
        if '2016' in dataset: e = '2016'
        elif '2017' in dataset: e = '2017'
        elif '2018' in dataset: e = '2018'
        elif '2022' in dataset: e = '2022'
        elif '2023' in dataset: e = '2023'
        else: 
          print(f'Era not found for {dataset}, exiting')
          exit()
        print(dataset, e)
        #get string RUN2022* from the dataset name
        run = re.search(rf"Run{e}[ABCDEFGHI]", dataset).group(0)
        
        #if run is F G H, then it is 2016postVFP
        if e == '2016' and 'HIPM' in dataset: e = '2016preVFP'
        elif e == '2016': e = '2016postVFP'
        
        if e == '2023' and 'D' in run: e = '2023BPix'
        elif e == '2023': e = '2023'
        
        

        
        #config.Data.unitsPerJob = getUnitsPerJob(dataset)
        print(f'dataset: {dataset}, era: {e}, run: {run}')
        config.JobType.scriptArgs.append(f'era={e}')
        requestName = e + "_" + run+"_" + dataset.split('/')[1]
        config.General.requestName = requestName
        config.Data.inputDataset = dataset
        crabCommand('submit', config = config)
        print(f"Submitted {requestName} ({i+1}/{len(samplelist)})")
        
    
    #samplelist = GetSampleList(open("MC_"+era+"_Vcb.txt"))
    samplelist = GetSampleList(open("QCDFesta.txt"))
    for i, dataset in enumerate(samplelist):
      config.JobType.scriptArgs = ['isData=0']
      e = ''
      if 'RunIISummer20UL16NanoAODAPV' in dataset: e = '2016preVFP'
      elif 'RunIISummer20UL16NanoAOD' in dataset: e = '2016postVFP'
      elif 'RunIISummer20UL17NanoAOD' in dataset: e = '2017'
      elif 'RunIISummer20UL18NanoAOD' in dataset: e = '2018'
      elif 'Run3Summer22NanoAODv12' in dataset: e = '2022'
      elif 'Run3Summer22EENanoAODv12' in dataset: e = '2022EE'
      elif 'Run3Summer23BPixNanoAOD' in dataset: e = '2023BPix'
      elif 'Run3Summer23NanoAOD' in dataset: e = '2023'
      else: 
        print(f'Era not found for {dataset}, exiting')
        exit()
      config.JobType.scriptArgs.append(f'era={e}')
      requestName = e + "_" + dataset.split('/')[1]
      #config.Data.unitsPerJob = getUnitsPerJob(dataset,1000000)
      
      print(f'dataset: {dataset}, era: {e}')
      #requestName = era
      config.General.requestName = requestName
      config.Data.inputDataset = dataset
      crabCommand('submit', config = config)
      print(f"Submitted {requestName} ({i+1}/{len(samplelist)})")
      
