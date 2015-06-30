import datetime
import os

import common_fxns
dConfig = common_fxns.parse_config('paths.ini')

sWorkingDir = dConfig['paths']['working_dir']
sDBDir = dConfig['paths']['db_dir']




def isolate():
    import isolate
    
    
    def all_cry_isolations():
        """
        isolates all audio samples, and saves and plots
        """
        
        sRoughDir = '{}/rough_db_files'.format(sWorkingDir)
        
        import os
        lLongCries = os.listdir(sRoughDir)
        lType = [s.split('-')[0] for s in lLongCries]
        
        
        for i in range(len(lType)):
            sCry = '{}/{}'.format(sRoughDir, lLongCries[i])
            sCutDir = '{}/DB_cries/{}'.format(sWorkingDir, lType[i])
            
            if not os.path.exists(sCutDir):
                os.makedirs(sCutDir)
            
            isolate.isolate_cries(sCry, sCutDir=sCutDir, bSave=True)
    
    
    
    oBegin = datetime.datetime.now()

    sCry = '{}/rough_db_files/{}'.format(sWorkingDir, "hungry-neh_all.wav")
    sCutDir = '{}/cut_cries'.format(sWorkingDir)
    
    isolate.isolate_cries(sCry, sCutDir, bSave = True)
    
    #all_cry_isolations()
    
    oEnd = datetime.datetime.now()
    
    print "Isolate Time:  ", (oEnd-oBegin)



def analyse():
    import analyse
    
    oBegin = datetime.datetime.now()


    import os

    sWorkingDir = '/home/roman/Critical_ID/classicry/classicry'
    sTypeDir = '{}/DB_cries'.format(sWorkingDir)

    sRecDir = '{}/{}/cut3.wav'.format(sTypeDir, 'hungry')
    sDBDir = '{}/{}/cut3.wav'.format(sTypeDir, 'burp')


    sCryType, iMisfit, iCorrArea = analyse.analyse_cry(sRecDir, sDBDir)


    oEnd = datetime.datetime.now()
    oDelta = oEnd - oBegin

    print 'Analyse Time:  ', oDelta




def classify():
    import classify
    oBegin = datetime.datetime.now()
    
    sType = 'burp'
    sRecDir = '{}/DB_cries/{}/cut3.wav'.format(sWorkingDir, sType)
    
    dAllSorted, dSortedTypes = classify.classify_cry(sRecDir)
    print sType, '\t', dSortedTypes['lsNames'][0:2],
    
    
    oEnd = datetime.datetime.now()
    print '\nclassify Time:  ', oEnd - oBegin
    
    



def check_all_cries():
    """
    run all cries against the database and return all results
    """
    import classify
    
    sCryDir = '/home/roman/Critical_ID/classicry/classicry/DB_cries'
    lsCryTypes = os.listdir(sCryDir)
    
    import datetime
    oBegin = datetime.datetime.now()
    
    dCries = {}
    
    for sCryType in lsCryTypes:
        sCutDir = '{0}/{1}'.format(sCryDir, sCryType)
        dCries[sCryType] = {}
        
        for sCut in os.listdir(sCutDir):
            sDir = '{0}/{1}/{2}'.format(sCryDir, sCryType, sCut)
            
            dAllSorted, dSortedTypes = classify.classify_cry(sDir)
            
            dCries[sCryType][sCut] = {
                'dAllSorted': dAllSorted, 
                'dSortedTypes': dSortedTypes
            }
    
    sOutputDir = '/home/roman/Critical_ID/classicry/classicry/classifications.txt'
    
    
    with open(sOutputDir, 'w+') as f:
        import json
        json.dump(dCries, f)
    
    oEnd = datetime.datetime.now()
    oDelta = oEnd - oBegin
    print 'Check all cries:  ', oDelta



def check_results():
    """check results of numeric comparison of signals"""
    sInput = '/home/roman/Critical_ID/classicry/classicry/classifications.txt'
    with open(sInput, 'r') as f:
        import json
        dCries = json.load(f)

    iTypeTrue = 0
    iTypeFalse = 0

    iTypeTopTrue = 0
    iTypeTopFalse = 0

    iTopsTrue = 0
    iTopsFalse = 0

    iTopsTopTrue = 0
    iTopsTopFalse = 0

    iORTrue = 0
    iORFalse = 0

    for sKey in dCries.keys():
        sType = sKey.split('-')[0]
        
        for sCut in dCries[sKey].keys():
            
            lTypeProbs = dCries[sKey][sCut]['dSortedTypes']['lsNames']
            lTypeConf = dCries[sKey][sCut]['dSortedTypes']['liConfidence']
            
            
            bType = (lTypeProbs[0] == sType)
            bTypeTop = sum([lTypeProbs[i]==sType for i in range(2)]) > 0     #if at least one is True
            
            
            if bType:
                iTypeTrue += 1
            else:
                iTypeFalse += 1
            
            if bTypeTop:
                iTypeTopTrue += 1
            else:
                iTypeTopFalse += 1
            
            
            
            
            
            print ' Guess:\t{} \t Input = {} \t{}  \t{}'.format(bType, sType,lTypeProbs, lTypeConf)
            
    print '\nNumber (Type) True:  {}\nNumber (Type) False:  {}'.format(iTypeTrue, iTypeFalse)
    print '\nNumber (Type top 2) True:  {}\nNumber (Type 3) False:  {}'.format(iTypeTopTrue, iTypeTopFalse)







oBegin = datetime.datetime.now()




#isolate()

#analyse()

#classify()

#check_all_cries()

#check_results()



oEnd = datetime.datetime.now()
print 'Total Time:  ', oEnd - oBegin















