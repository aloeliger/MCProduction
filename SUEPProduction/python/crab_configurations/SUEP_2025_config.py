from CRABClient.UserUtilities import config
import os
import datetime

today = datetime.date.today().strftime('%d%b%Y')
cmssw_base = os.getenv('CMSSW_BASE')
total_events = 100000

config = config()

config.General.requestName = f'SUEP_GEN_SIM_RAW_{today}'
config.General.workArea = './crab'
config.General.transferOutputs = True

config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = f'{cmssw_base}/src/MCProduction/SUEPProduction/python/paper_2025_fragments_and_examples/suep_fragment_py_GEN_SIM_DIGI_L1_DIGI2RAW_HLT_PU.py'
config.JobType.maxMemoryMB = 4000

config.Data.outputPrimaryDataset='SUEP'
config.Data.splitting='EventBased'
config.Data.unitsPerJob = 50
config.Data.totalUnits = total_events
config.Data.outputDatasetTag = f'SUEP_GEN_SIM_RAW_{today}'

config.Site.storageSite = 'T2_US_Wisconsin'
