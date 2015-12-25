#!/usr/bin/python

import time
import os
import locale
locale.setlocale(locale.LC_ALL, 'en_US')
from subprocess import Popen, PIPE
import numpy as np

pdNames=["HIMinimumBias1"]
pdNames.append("HIMinimumBias2")
pdNames.append("HIMinimumBias3")
pdNames.append("HIMinimumBias4")
pdNames.append("HIMinimumBias5")
pdNames.append("HIMinimumBias6")
pdNames.append("HIMinimumBias7")
pdNames.append("HIMinimumBias8")
pdNames.append("HIMinimumBias9")
pdNames.append("HIMinimumBias10")
pdNames.append("HIMinimumBias11")
pdNames.append("HIForward")
pdNames.append("HIPhoton40AndZ")
pdNames.append("HIEWQExo")
pdNames.append("HIOniaCentral30L2L3")
pdNames.append("HIOniaPeripheral30100")
pdNames.append("HIOniaL1DoubleMu0")
pdNames.append("HIOniaL1DoubleMu0B")
pdNames.append("HIOniaL1DoubleMu0C")
pdNames.append("HIOniaL1DoubleMu0D")
pdNames.append("HIHardProbes")
pdNames.append("HIHardProbesPeripheral")
pdNames.append("HIHardProbesPhotons")
pdNames.append("HIFlowCorr")
pdNames.append("HIOniaTnP")

fileOutputPD = open("sizeForPD.txt","a")
fileOutputPD.write(time.strftime("%m/%d/%Y-%H:%M"))
totalSize = [0] * 4
for pdName in pdNames:
    dasRAWPathName = '/' + pdName + '/HIRun2015-PromptReco-v1/AOD | grep dataset.size, dataset.nevents, dataset.nlumis, dataset.nfiles'
    rawCommand = 'python das.py --limit=1000 --format=plain --query="dataset dataset=' + dasRAWPathName + '" >tmp.txt ; tail -1 tmp.txt > size.txt'
    os.system(rawCommand)

    fileInput = open("size.txt", "r")
    theValue = []
    val=[]
    for val in fileInput.read().split():
        if(val == '[]'):
            val = 0
        theValue.append(float(val))
    fileOutputPD.write("   ")
    fileOutputPD.write(str(theValue[0]*(1e-12)))
    fileOutputPD.write("   ")
    fileOutputPD.write(str(theValue[1]*(1e-6)))
    fileOutputPD.write("   ")
    fileOutputPD.write(str(theValue[2]*(1)))
    fileOutputPD.write("   ")
    fileOutputPD.write(str(theValue[3]*(1)))
    #print theValue
    totalSize[0] += theValue[0]*(1e-12)
    totalSize[1] += theValue[1]*(1e-6)
    totalSize[2] += theValue[2]*(1)
    totalSize[3] += theValue[3]*(1)
    fileInput.close()


fileOutput = open("volumeEventSize.txt","a")
fileOutput.write(time.strftime("%m/%d/%Y-%H:%M"))
i=0
while i<len(totalSize):
    fileOutput.write("   ")
    fileOutput.write(str(totalSize[i]))
    fileOutputPD.write("   ")
    fileOutputPD.write(str(totalSize[i]))
    i +=1

fileOutput.write("\n")
fileOutputPD.write("\n")


