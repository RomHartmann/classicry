def analyse_cry(xRec, xDB):
    """
    inputs must either be path string or dictionary of form:
    dInput = {
            'iSampleRate': iSampleRate,
            'aTime': aTime,
            'aAudio': aAudio,
            'aCorr': aCorr
        }
    Correlation and least squares comparison between audio files
    classifications based on classifications by Pricilla Dunstan
    """
    import numpy as np
    from scipy import signal
    
    import common_fxns
    
    def normalize(aArray):
        iMax = np.max(aArray)
        return [i/iMax for i in aArray]
    
    
    def calc_misfit(a1, a2):
        """
        calculates the misfit between the 2 arrays and returns a scalar
        shortest array length is taken
        """
        iLen = len(a1) if len(a1)<len(a2) else len(a2)
        
        iMisfit = 0
        for i in range(iLen):
            iMisfit += (a1[i] - a2[i])**2
        return iMisfit
    
    
    def round_sci(iNum, iSigs):
        """
        round number to significant figures
        """
        return float(format(iNum, '.{0}g'.format(iSigs)))
    
    
    if type(xRec) == str:
        sRecDir = xRec
        (iRecSampleRate, 
            aRecTime_NoShift, 
            aRecAudio, 
            aRecCorr_NoShift) = common_fxns.process_dir(sRecDir)[0:4]
        
    elif type(xRec) == dict:
        iRecSampleRate = xRec['iSampleRate']
        aRecTime_NoShift = xRec['aTime']
        aRecAudio = xRec['aAudio']
        aRecCorr_NoShift = xRec['aCorr']
        
    else:
        raise ValueError('Please enter a string or dict of the correct format')
    
    
    
    
    if type(xDB) == str:
        sDBDir = xDB
        (iDBSampleRate, 
            aDBTime_NoShift, 
            aDBAudio, 
            aDBCorr_NoShift) = common_fxns.process_dir(sDBDir)[0:4]
        
    elif type(xDB) == dict:
        iDBSampleRate = xDB['iSampleRate']
        aDBTime_NoShift = xDB['aTime']
        aDBAudio = xDB['aAudio']
        aDBCorr_NoShift = xDB['aCorr']
        
    else:
        raise ValueError('Please enter a string or dict of the correct format')
    
    
    
    
    
    aRecCorr_NoShift = normalize(aRecCorr_NoShift)
    aDBCorr_NoShift = normalize(aDBCorr_NoShift)
    
    
    
    #shifted guassian correlations such that misfit has more meaning
    #shifted such that maxima line up
    iIndexMax = np.argmax(aRecCorr_NoShift)
    iDBIndexMax = np.argmax(aDBCorr_NoShift)
    
    #always shifting right: therefore shift where argmax is less
    #for y values, prepend 0, for tive values, prepend time increments
    if iDBIndexMax > iIndexMax:
        #shift signal 1 to the right
        iShift = iDBIndexMax - iIndexMax
        aRec = np.zeros(len(aRecCorr_NoShift) + iShift)
        aRec[iShift:] = aRecCorr_NoShift
        
        aRecTime = np.zeros(len(aRecTime_NoShift) + iShift)
        aRecTime[:iShift] = np.array([i/iRecSampleRate for i in range(iShift)])
        aRecTime[iShift:] = aRecTime_NoShift + iShift/iRecSampleRate
        
        aDB = aDBCorr_NoShift
        aDBTime = aDBTime_NoShift
    else:
        #shift signal 2 to the right
        iShift = iIndexMax - iDBIndexMax
        aDB = np.zeros(len(aDBCorr_NoShift) + iShift)
        aDB[iShift:] = aDBCorr_NoShift
        
        aDBTime = np.zeros(len(aDBTime_NoShift) + iShift)
        aDBTime[:iShift] = np.array([i/iDBSampleRate for i in range(iShift)])
        aDBTime[iShift:] = aDBTime_NoShift + iShift/iDBSampleRate
        
        aRec = aRecCorr_NoShift
        aRecTime = aRecTime_NoShift
    
    
    
    #correlation between 2 signals
    aCorr = np.correlate(aRec, aDB, 'same')
    aCorrTime = aRecTime if len(aRecTime) > len(aDBTime) else aDBTime
    
    #least squares comparison to get misfit
    iMisfit = calc_misfit(aRec, aDB)
    iCorrArea = np.trapz(aCorr, aCorrTime)
    
    #round to 3 significant figures
    iMisfit = round_sci(iMisfit, 3)
    iCorrArea = round_sci(iCorrArea, 3)
    
    
    
    
    return iMisfit, iCorrArea


















