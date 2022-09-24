# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: Configuration/Generator/python/defaultFragment.py --fileout file:out.root --mc --eventcontent RAWSIM --datatier GEN-SIM --conditions 124X_mcRun3_2022_realistic_v10 --beamspot Realistic25ns13p6TeVEarly2022Collision --step GEN,SIM --geometry DB:Extended --era Run3 --no_exec
import FWCore.ParameterSet.Config as cms

import FWCore.ParameterSet.VarParsing as VarParsing
options = VarParsing.VarParsing('analysis')
options.register('jobNum', 0, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, 'Job number for tasks involving multiple generation jobs. Defaults to 1')
options.parseArguments()

from Configuration.Eras.Era_Run3_cff import Run3

process = cms.Process('SIM',Run3)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.GeometrySimDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic25ns13p6TeVEarly2022Collision_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
        input = cms.untracked.int32(100),
        output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

# Input source
process.source = cms.Source("EmptySource")
#The runSVJ script modifies this with:
#process.source.firstEvent = cms.untracked.uint32((options.part-1)*options.maxEvents+1)
#what is options.part?
#seems to default to 1?
#the readme describes it as: part number when producing a sample in multiple jobs

#handle the random seed so we don't get multiple copies of the same file in a large run
#but have reproducible results if necessary

from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper
randHelper = RandomNumberServiceHelper(process.RandomNumberGeneratorService)
randHelper.resetSeeds(1234+options.jobNum)

#This is removed entirely in the SUEP configuration
process.options = cms.untracked.PSet(
    FailPath = cms.untracked.vstring(),
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring(),
    SkipEvent = cms.untracked.vstring(),
    accelerators = cms.untracked.vstring('*'),
    allowUnscheduled = cms.obsolete.untracked.bool,
    canDeleteEarly = cms.untracked.vstring(),
    deleteNonConsumedUnscheduledModules = cms.untracked.bool(True),
    dumpOptions = cms.untracked.bool(False),
    emptyRunLumiMode = cms.obsolete.untracked.string,
    eventSetup = cms.untracked.PSet(
        forceNumberOfConcurrentIOVs = cms.untracked.PSet(
            allowAnyLabel_=cms.required.untracked.uint32
        ),
        numberOfConcurrentIOVs = cms.untracked.uint32(0)
    ),
    fileMode = cms.untracked.string('FULLMERGE'),
    forceEventSetupCacheClearOnNewRun = cms.untracked.bool(False),
    makeTriggerResults = cms.obsolete.untracked.bool,
    numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(0),
    numberOfConcurrentRuns = cms.untracked.uint32(1),
    numberOfStreams = cms.untracked.uint32(0),
    numberOfThreads = cms.untracked.uint32(1),
    printDependencies = cms.untracked.bool(False),
    sizeOfStackForThreadsInKB = cms.optional.untracked.uint32,
    throwIfIllegalParameter = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('Configuration/Generator/python/defaultFragment.py nevts:1'), #They use something called EmptyFragment_cff.py in their setup. It is basically what I have, modulo some era differences?
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.RAWSIMoutput = cms.OutputModule("PoolOutputModule",
                                        SelectEvents = cms.untracked.PSet(
                                                SelectEvents = cms.vstring('generation_step')
                                        ),
    compressionAlgorithm = cms.untracked.string('LZMA'),
                                        compressionLevel = cms.untracked.int32(1),
                                        dataset = cms.untracked.PSet(
                                                dataTier = cms.untracked.string('GEN-SIM'), #they default to GEN, but I think we can do GEN-SIM
                                                filterName = cms.untracked.string('')
                                        ),
    eventAutoFlushCompressedSize = cms.untracked.int32(20971520),
                                        fileName = cms.untracked.string(options.outputFile),
                                        outputCommands = process.RAWSIMEventContent.outputCommands,
                                        splitLevel = cms.untracked.int32(0)
)

# Additional output definition

# Other statements
#these next two statements are not present in the SUEP configuration
if hasattr(process, "XMLFromDBSource"): process.XMLFromDBSource.label="Extended"
if hasattr(process, "DDDetectorESProducerFromDB"): process.DDDetectorESProducerFromDB.label="Extended"
process.genstepfilter.triggerConditions=cms.vstring("generation_step")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '124X_mcRun3_2022_realistic_v10', '')

process.generator = cms.EDFilter("Pythia8ConcurrentGeneratorFilter",
    PythiaParameters = cms.PSet(
            #They have additional pythi8PSweightSettings present here
        parameterSets = cms.vstring(
            'pythia8CommonSettings',
            'pythia8CP5Settings',
            'processParameters'
        ),
            #They do not have this
        processParameters = cms.vstring('SoftQCD:inelastic = on'),
        pythia8CP5Settings = cms.vstring(
            'Tune:pp 14',
            'Tune:ee 7',
            'MultipartonInteractions:ecmPow=0.03344',
            'MultipartonInteractions:bProfile=2',
            'MultipartonInteractions:pT0Ref=1.41',
            'MultipartonInteractions:coreRadius=0.7634',
            'MultipartonInteractions:coreFraction=0.63',
            'ColourReconnection:range=5.176',
            'SigmaTotal:zeroAXB=off',
            'SpaceShower:alphaSorder=2',
            'SpaceShower:alphaSvalue=0.118',
            'SigmaProcess:alphaSvalue=0.118',
            'SigmaProcess:alphaSorder=2',
            'MultipartonInteractions:alphaSvalue=0.118',
            'MultipartonInteractions:alphaSorder=2',
            'TimeShower:alphaSorder=2',
            'TimeShower:alphaSvalue=0.118',
            'SigmaTotal:mode = 0',
            'SigmaTotal:sigmaEl = 22.08', #This value is slightly different in their config
            'SigmaTotal:sigmaTot = 101.037', #as is this
            'PDF:pSet=LHAPDF6:NNPDF31_nnlo_as_0118'
        ),
            #they also have:
            #SLHA:keepSM = on
        pythia8CommonSettings = cms.vstring(
            'Tune:preferLHAPDF = 2',
            'Main:timesAllowErrors = 10000',
            'Check:epTolErr = 0.01',
            'Beams:setProductionScalesFromLHEF = off',
            'SLHA:minMassSM = 1000.',
            'ParticleDecays:limitTau0 = on',
            'ParticleDecays:tau0Max = 10',
            'ParticleDecays:allowPhotonRadiation = on'
        )
            #They then have a huge set of pythia8PSweightsSettings here
    ),
    comEnergy = cms.double(13600.0),
    filterEfficiency = cms.untracked.double(1.0),
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    pythiaPylistVerbosity = cms.untracked.int32(1)
)
process.generator.crossSection = cms.untracked.double(1.0)
process.generator.PythiaParameters.processParameters = cms.vstring(
        'Check:event = off',
        # parameters for mediator (Higgs)
        'Higgs:useBSM = on',
        'HiggsBSM:gg2H1 = on',
        'HiggsH1:coup2d = 1',
        'HiggsH1:coup2u = 0',
        'HiggsH1:coup2Z = 0',
        'HiggsH1:coup2W = 0',
        'HiggsH1:coup2l = 0',
        #'{}:m0 = {:g}'.format(self.idMediator,self.mMediator),
        '{}:m0 = {:g}'.format(25, 125.0),
        # add a dark meson and dark photon 
        #'{}:all = GeneralResonance void 0 0 0 {:g} 0.001 0.0 0.0 0.0'.format(self.idDark,self.mDark),
        '{}:all = GeneralResonance void 0 0 0 {:g} 0.001 0.0 0.0 0.0'.format(999999, 2.0),
        #'{}:all = GeneralResonance void 1 0 0 {:g} 0.001 0.0 0.0 0.0'.format(self.idPho,self.mPho),
        '{}:all = GeneralResonance void 1 0 0 {:g} 0.001 0.0 0.0 0.0'.format(999998, 1.),
        # define dark meson decay
        '{}:addChannel = 1 1.0 101 {} {} '.format(999999, 999998, 999998), # 100% br to dark photons
        '{}:addChannel = 1 1.0 101 211 -211 '.format(999998) #100% br to pi+ pi-
)
process.generator.UserCustomization = cms.VPSet(
        cms.PSet(
                pluginName = cms.string("SuepDecay"),
                #temperature = cms.double(self.temperature),
                temperature = cms.double(2.0),
                idMediator = cms.int32(25),
                idDark = cms.int32(999999),
        )
)

#The SUEP config then does some stuff to this generator
#   process.generator.crossSection = cms.untracked.double(_helper.xsec)
#this pulls from the SUEP helper, where eventually the xsec is just 1?
# but there is also this thing here:
#
#Then it does:
#    process.generator.PythiaParameters.processParameters = csm.vstring(_helper.getPythiaSettings())
#this, when pulled from the SUEP helper is
    # def getPythiaSettings(self):
    #     # todo: include safety/sanity checks
    #     if self.decay!="generic" and self.decay!="darkPho" and self.decay!="darkPhoHad": 
    #         raise ValueError("Unknown decay mode: "+self.decay)
    #     if 2.0*self.mPho > self.mDark : 
    #         raise ValueError("dark photon mass {} more than 2x dark meson mass {}".format(self.mPho, self.mDark) )
    #     # We decay each dark meson two 2 dark photons (pdg code 999998) 
    #     # Each dark photon in turn decays to SM fermions
    #     # The dark photon branching ratios are mass dependent, 
    #     # see e.g. arxiv:1505.07459. Values used here are approximate.
    #     lines = [
    #         'Check:event = off',
    #         # parameters for mediator (Higgs)
    #         'Higgs:useBSM = on',
    #         'HiggsBSM:gg2H1 = on',
    #         'HiggsH1:coup2d = 1',
    #         'HiggsH1:coup2u = 0',
    #         'HiggsH1:coup2Z = 0',
    #         'HiggsH1:coup2W = 0',
    #         'HiggsH1:coup2l = 0',
    #         '{}:m0 = {:g}'.format(self.idMediator,self.mMediator),
    #         # add a dark meson and dark photon 
    #         '{}:all = GeneralResonance void 0 0 0 {:g} 0.001 0.0 0.0 0.0'.format(self.idDark,self.mDark),
    #         '{}:all = GeneralResonance void 1 0 0 {:g} 0.001 0.0 0.0 0.0'.format(self.idPho,self.mPho),
    #         # define dark meson decay
    #         '{}:addChannel = 1 1.0 101 {} {} '.format(self.idDark,self.idPho,self.idPho), # 100% br to dark photons
    #     ]

    #     # define dark photon decay
    #     if self.decay=="darkPho":
    #         lines.append('{}:addChannel = 1 0.40 101 11 -11 '.format(self.idPho)  )#40% br to e+ e-
    #         lines.append('{}:addChannel = 1 0.40 101 13 -13 '.format(self.idPho)  )#40% br to m+ m-
    #         lines.append('{}:addChannel = 1 0.20 101 211 -211 '.format(self.idPho))#20% br to pi+ pi-
    #     elif self.decay=="darkPhoHad":
    #         lines.append('{}:addChannel = 1 0.15 101 11 -11 '.format(self.idPho)  )#15% br to e+ e-
    #         lines.append('{}:addChannel = 1 0.15 101 13 -13 '.format(self.idPho)  )#15% br to m+ m-
    #         lines.append('{}:addChannel = 1 0.70 101 211 -211 '.format(self.idPho))#70% br to pi+ pi-
    #     else : # "generic" uubar
    #         lines.append('{}:addChannel = 1 1.0 101 211 -211 '.format(self.idPho)) #100% br to pi+ pi-
# Then it goes on to do some thing like:
                # process.generator.UserCustomization = cms.VPSet(
                #     _helper.getHookSettings()
                # )
#which is defined in the helper as:
    # def getHookSettings(self):
    #     pset = cms.PSet(
    #         pluginName = cms.string("SuepDecay"),
    #         temperature = cms.double(self.temperature),
    #         idMediator = cms.int32(self.idMediator),
    #         idDark = cms.int32(self.idDark),
    #     )



#The SUEP config has a statement here to the effect of:
#process.ProductionFilterSequence = cms.Sequence(process.generator)

# Path and EndPath definitions
process.generation_step = cms.Path(process.pgen)
process.simulation_step = cms.Path(process.psim) #This is extra to us, for the sim step
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary) #this is extra to us
process.endjob_step = cms.EndPath(process.endOfProcess)
process.RAWSIMoutput_step = cms.EndPath(process.RAWSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step,process.simulation_step,process.endjob_step,process.RAWSIMoutput_step) #this is in essence the same, except for the sim step
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)
# filter all path with the production filter sequence
for path in process.paths:
	getattr(process,path).insert(0, process.generator) #this is ProductionFilterSequence in the SUEP config



# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
