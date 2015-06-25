from datetime import datetime as dt
import os

import common_fxns
dConfig = common_fxns.parse_config('paths.ini')

sWorkingDir = dConfig['paths']['working_dir']
sDBDir = dConfig['paths']['db_dir']
sCutDir = dConfig['paths']['cut_dir']




def check_file(sInput, iResample, bSave, sCutDir):
    """do entire process for one audio file"""
    
    sType = sInput.split('-')[0].split('/')[-1]

    #edge detection on the recording, isolate the cry(s)
    #either save result to disk or return results
    import isolate
    iSampleRate, laAudios, laCorrs = isolate.isolate_cries(sInput, sCutDir=sCutDir, bSave=bSave, iResample=iResample)

    dAggregatedCries = {}
    
    iTrue = 0
    iFalse = 0
    
    #run returned samples against database
    import classify
    if bSave:
        lsCuts = os.listdir(sCutDir)
        for sCut in lsCuts:
            sCryDir = '{}/{}'.format(sCutDir, sCut)
            
            dAllSorted, dSortedTypes = classify.classify_cry(sCryDir)
            print sType, '\t', dSortedTypes['lsNames'], dSortedTypes['liValues']

    else:
        for i in range(len(laAudios)):
            
            import numpy as np
            aAudio = laAudios[i]
            aCorr = laCorrs[i]
            aTime = np.array( [float(i)/iSampleRate for i in range(len(aAudio))] )
            
            dInput = {
                'iSampleRate': iSampleRate,
                'aTime': aTime,
                'aAudio': aAudio,
                'aCorr': aCorr
            }
            
            dAllSorted, dSortedTypes = classify.classify_cry(dInput)
            
            for i in range(len(dSortedTypes['lsNames'])):
                sCryType = dSortedTypes['lsNames'][i]
                sCryVal = dSortedTypes['liConfidence'][i]
                
                try:
                    dAggregatedCries[sCryType] += sCryVal
                except KeyError:
                    dAggregatedCries[sCryType] = sCryVal
            
            bEqual = sType == dSortedTypes['lsNames'][0]
            if bEqual:
                iTrue+=1
            else:
                iFalse+=1
            
            #print bEqual, sType, '\t', dSortedTypes['lsNames'],  dSortedTypes['liConfidence']
            #print '\t', dAllSorted['lsNames'][0:5], dAllSorted['liValues'][0:5]
    
    
    lAggregatedNames = [x for (y,x) in sorted(zip(dAggregatedCries.values() ,dAggregatedCries.keys()), reverse=True)]
    lAggregatedValues = [round(y,2) for (y,x) in sorted(zip(dAggregatedCries.values() ,dAggregatedCries.keys()), reverse=True)]
    
    
    #print "---aggregated:  ", sType, lAggregatedNames, lAggregatedValues
    #print "true:false", iTrue, iFalse
    
    return iTrue, iFalse
    


def create_db(iResample):
    """create database audio files at iResample iSampleRate"""
    
    import isolate
    sRoughDir = '{}/rough_db_files'.format(sWorkingDir)
    import os
    lLongCries = os.listdir(sRoughDir)
    lType = [s.split('-')[0] for s in lLongCries]
    
    for i in range(len(lType)):
    #for i in range(1):
        #i=3
        
        sCutDir = '{}/DB_cries/{}'.format(sWorkingDir, lType[i])
        sInput = '{}/{}'.format(sRoughDir, lLongCries[i])
        
        if not os.path.exists(sCutDir):
            os.makedirs(sCutDir)
            
        isolate.isolate_cries(sInput, sCutDir=sCutDir, bSave=True, iResample=iResample)
    
    
    
    
def check_all(iResample):
    sRoughDir = '{}/rough_db_files'.format(sWorkingDir)
    lAllRough = os.listdir(sRoughDir)
    
    iGlobTrue = 0
    iGlobFasle = 0
    
    for sFile in lAllRough:
        sInput = '{}/{}'.format(sRoughDir, sFile)
        iTrue, iFalse = check_file(sInput, bSave=False, iResample=iResample, sCutDir=sCutDir)
        
        iGlobTrue += iTrue
        iGlobFasle += iFalse
        
    print "\n Global true:false", iGlobTrue, iGlobFasle



oBegin = dt.now()

iResample=8000
print "\n Resample Rate:  ", iResample

create_db(iResample)

print 'Create DB Time:  ', dt.now() - oBegin

sInput = '{}/rough_db_files/{}'.format(sWorkingDir, "burp-eh_all.wav")

#check_file(sInput, bSave=False, iResample=iResample, sCutDir=sCutDir)

check_all(iResample)





print 'Total Time:  ', dt.now() - oBegin













