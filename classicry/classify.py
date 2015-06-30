def classify_cry(xRec):
    """
    compare a cry to all pre-identified cries
    xRec is either path string or dictionary of form:
        dInput = {
            'iSampleRate': iSampleRate,
            'aTime': aTime,
            'aAudio': aAudio,
            'aCorr': aCorr
        }
    
    """
    import analyse
    import os
    
    iSelfCorrArea = analyse.analyse_cry(xRec, xRec)[1]
    
    lsCryNames = []
    liCryValues = []
    
    dCries = {}
    
    import common_fxns
    dConfig = common_fxns.parse_config('paths.ini')
    sCryDir = dConfig['paths']['db_dir']
    lsCryTypes = os.listdir(sCryDir)
    
    for sCryType in lsCryTypes:
        sCutDir = '{0}/{1}'.format(sCryDir, sCryType)
        
        for sCut in os.listdir(sCutDir):
            sDBDir = '{0}/{1}/{2}'.format(sCryDir, sCryType, sCut)
            
            iMisfit, iCorrArea = analyse.analyse_cry(xRec, sDBDir)
            
            iDeltaArea = abs(iCorrArea - iSelfCorrArea)
            iComparisonMetric = iMisfit * iDeltaArea
            
            lsCryNames.append(sCryType)
            liCryValues.append(iComparisonMetric)
            
            try:
                dCries[sCryType] += iComparisonMetric
            except KeyError:
                dCries[sCryType] = iComparisonMetric
    
    
    lsCryNamesSorted = [x for (y,x) in sorted(zip(liCryValues,lsCryNames))]
    liCryValuesSorted = [round(y,2) for (y,x) in sorted(zip(liCryValues,lsCryNames))]
    
    dAllSorted = {
        'lsNames': lsCryNamesSorted,
        'liValues': liCryValuesSorted
    }
    
    
    
    lsAllTopsSortedNames = [x for (y,x) in sorted(zip(dCries.values(), dCries.keys()))]
    liAllTopsSortedValues = [round(y,2) for (y,x) in sorted(zip(dCries.values(), dCries.keys()))]
    
    
    liConfidence = common_fxns.get_confidence(liAllTopsSortedValues)
    
    #aggregated and sorted results based on all comparisons, with normalized confidence results
    dSortedTypes = {
        'lsNames': lsAllTopsSortedNames,
        'liValues': liAllTopsSortedValues,
        'liConfidence': liConfidence
    }
    
    
    return dAllSorted, dSortedTypes















