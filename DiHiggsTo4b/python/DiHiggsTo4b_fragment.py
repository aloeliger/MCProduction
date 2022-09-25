import FWCore.ParameterSet.Config as cms
externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
                                     args = cms.vstring('/hdfs/store/user/aloeliger/DiHiggsTo4b_13p6TeV_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz'),
                                     #args = cms.vstring('/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc481/14TeV/madgraph/V5_2.3.3/GF_HH_SM_14Tev/v1/GF_HH_SM_14Tev_tarball.tar.xz','false','slc6_amd64_gcc481','CMSSW_7_1_29'),
                                     nEvents = cms.untracked.uint32(5000),
                                     numberOfParameters = cms.uint32(1),
                                     outputFile = cms.string('cmsgrid_final.lhe'),
                                     scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
                                     )
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
                         maxEventsToPrint = cms.untracked.int32(1),
                         pythiaPylistVerbosity = cms.untracked.int32(1),
                         filterEfficiency = cms.untracked.double(1.0),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         comEnergy = cms.double(14000.),
                         PythiaParameters = cms.PSet(
                                                    pythia8CommonSettingsBlock,
                                                     pythia8CP5SettingsBlock,
                                                     processParameters = cms.vstring(
                                                                                    '25:onMode = off',
                                                                                     '25:onIfMatch = 5 -5',
                                                                                     'ResonanceDecayFilter:filter = on'
                                                                                     ),
                                                     parameterSets = cms.vstring('pythia8CommonSettings',
                                                                                'pythia8CP5Settings',
                                                                                 'processParameters'
                                                                                 )
                                                     )
                         )
ProductionFilterSequence = cms.Sequence(generator)
