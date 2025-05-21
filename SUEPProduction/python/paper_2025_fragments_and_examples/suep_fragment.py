import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi import *

generator = cms.EDFilter("Pythia8ConcurrentGeneratorFilter",
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

generator.crossSection = cms.untracked.double(1.0)
generator.PythiaParameters.processParameters = cms.vstring(
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
generator.UserCustomization = cms.VPSet(
        cms.PSet(
                pluginName = cms.string("SuepDecay"),
                #temperature = cms.double(self.temperature),
                temperature = cms.double(2.0),
                idMediator = cms.int32(25),
                idDark = cms.int32(999999),
        )
)
