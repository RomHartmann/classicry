def smooth(aSignal, iWindowSize):
    """
    smooth a signal by window size using kernel operator
    """
    import numpy as np
    aKernel = np.ones(int(iWindowSize))/float(iWindowSize)
    return np.convolve(aSignal, aKernel, 'same')




def audio2array(sDir, iResample=None):
    """
    Returns monotone data for a wav audio file in form:  
        iSampleRate, aNumpySignalArray, aNumpyTimeArray
    iResample is the new resampling rate desired
    
    """
    from scipy.io.wavfile import read
    import numpy as np
    
    lAudio = read(sDir)
    iSampleRate, aAudio = lAudio
    iSampleRate = float(iSampleRate)
    
    #make monotone
    try:
        len(aAudio[0])
        bLen = True
    except TypeError:
        bLen = False
    
    if bLen and len(aAudio[0]) == 2:
        aAudio = np.array([ (l[0]+l[1])/2 for l in aAudio])
    else:
        aAudio = np.array(aAudio)
    
    
    aTime = np.array( [float(i)/iSampleRate for i in range(len(aAudio))] )
    
    if iResample != None:
        #from scipy import signal
        #iSecs = len(aTime)/iSampleRate
        #aAudio = signal.resample(aAudio, iSecs*iResample)
        #aTime = signal.resample(aTime, iSecs*iResample)
        #iSampleRate = iResample
        
        aAudio = downsample(aAudio, iSampleRate, iResample)
        aTime = downsample(aTime, iSampleRate, iResample)
        iSampleRate = iResample
        
    return iSampleRate, aTime, aAudio





def process_dir(sDir, iResample=None, iSmooth = 50, iSigmaSecs=0.01):
    """
    take input dir and output smoothed, correlated array
    iSigmaSecs:  standard deviation of gaussian in seconds
    iSmooth = smoothing window size for linear smoother
    """
    from scipy import signal
    import numpy as np
    iSampleRate, aTime, aOrigAudio = audio2array(sDir, iResample)
    
    #only positive
    aAudio = [abs(i) for i in aOrigAudio]
    
    #audio files must be right format
    aOrigAudio = np.asarray(aOrigAudio, dtype=np.int16)
    
    if not iSmooth == None:
        #smooth
        aAudio = smooth(aAudio, iSmooth)
    
    #standard deviation for gaussian function
    iSigma = float(iSigmaSecs * iSampleRate)
    aGaussian = signal.gaussian(10*iSigma, iSigma)
    
    #gaussian correlated with audio signal
    aCorr = np.correlate(aAudio, aGaussian, 'same')
    
    
    return iSampleRate, aTime, aAudio, aCorr, aOrigAudio






def downsample(aSignal, iOldRate, iNewRate):
    """
    downsample array to lower rate
    """
    from scipy import interpolate
    import numpy as np
    iLen = float(len(aSignal))
    iEnd = iLen/iOldRate
    
    aX = np.arange(0, iEnd, 1.0/iOldRate)
    f = interpolate.interp1d(aX, aSignal)
    
    aNewX = np.arange(0, iEnd, 1.0/iNewRate)
    aNewY = f(aNewX)
    
    return aNewY




def parse_config(sFileName):
    """
    parse .ini file and return dictionary
    """
    import ConfigParser
    oConfig = ConfigParser.ConfigParser()
    oConfig.read(sFileName)
    dConfig = oConfig.__dict__['_sections'].copy()
    
    return dConfig





def get_confidence(lValues):
    """
    returns a list with sum=0 that gives a relative get_confidence
    with respect to each other.  High values are good confidence, 
    large negatives are low confidence
    """
    iSum = float(sum(lValues))
    iLen = float(len(lValues))
    liConfidence = [(1- (i/(iSum)))/(iLen-1) for i in lValues]
    #normailize confidence wrt to mean
    iMean = 1.0/len(liConfidence)
    liConfidence = [round((i-iMean)*100, 2) for i in liConfidence]
    
    return liConfidence









