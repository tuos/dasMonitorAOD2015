#!/usr/bin/env python
#
# Script to print information about the locations and numbers of files for heavy ion AOD datasets from a DAS wildcard listing
# December 11, 2016
# execute "voms-proxy-init -rfc -voms cms" before running the script
# a das_client.py script must be in the working directory
#
# Usage:  type python printHIAODSites.py --title <'Name of the datasets'> --nPDs <numberOfPDsToProcess>
#         the --title option is followed by a descriptive name of the datasets
#         if the --title option is omitted, a generic description is used 'HI AOD File Set'
#         If all the PDs in the list of AODs are to be processed, the --nPDs option can be omitted; otherwise it should be a positive number
#         type  python printHIAODSites.py --help   to get a help message
#
# Operation: A list of datasets is read from a text file named listOfAODs.txt in the working directory
#
# Ouput: A nine column table is printed with rows according to the PD name
#        The columns include the volume, number of files, and number of events in the PD
#        The number of T2 sites storing replica parts of the PD and the fraction sizes of these site replicas
#        The amount of storage of the PD on disk at the Vanderbilt site is always given
#        The amount of storage of the PD on tape at the FNAL site is always given
#        The total amount of PD volume which exists only at Vanderbilt is calculated
#        The amount of PD volume replicated at other T2 sites is tabulated; note the replications could be identical blocks at more than one external T2 site
#        The amount of PD volume on tape at FNAL is caculated
#

from datetime import datetime
import os
import argparse                       # argument parser library
from prettytable import PrettyTable
from prettytable import ALL

import pwd
from shutil import copyfile

import getpass

Dir = os.path.dirname(os.path.realpath(__file__))

def exitLoop(ncycle):
    limit = 6
    return True if ncycle == limit else False

def findNEvents(path, dataset):
    ncycle = 0
    notFind = True
    nEvents = -99
    while not exitLoop(ncycle) and  notFind:
        findNEventsCommand = 'python ' + path + '/das_client.py --limit=1000 --format=plain --query="dataset dataset=' + dataset + ' | grep dataset.nevents" > tmp.txt ; tail -1 tmp.txt > pdEvents.txt'
        os.system(findNEventsCommand)
        fileInput = open('pdEvents.txt','r')
        for line in fileInput:
            number = line.rstrip()
            if not number.strip() :
                return 0
            try:
                nEvents = int(number)     
                notFind = False
            except ValueError:
                print "Oops! Got an invalid output for findNEvents. Let me try again..."
                ncycle += 1
        fileInput.close()
    return nEvents

def findNFiles(path, dataset):
    ncycle = 0
    notFind = True
    nFiles = -99
    while not exitLoop(ncycle) and  notFind:
        findNFilesCommand = 'python ' + path + '/das_client.py --limit=1000 --format=plain --query="dataset dataset=' + dataset + ' | grep dataset.nfiles" > tmp.txt ; tail -1 tmp.txt > pdNfiles.txt'
        os.system(findNFilesCommand)
        fileInput = open('pdNfiles.txt','r')
        for line in fileInput:
            number = line.rstrip()
            if not number.strip() :
                return 0
            try:
                nFiles = int(number)     
                notFind = False
            except ValueError:
                print "Oops! Got an invalid output for findNFiles. Let me try again..."
                ncycle += 1
        fileInput.close()
    return nFiles

def findPDVolume(path, dataset):
    ncycle = 0
    notFind = True
    pdVolume = -99
    while not exitLoop(ncycle) and  notFind:
        findPDVolumeCommand = 'python ' + path + '/das_client.py --limit=1000 --format=plain --query="dataset dataset=' + dataset + ' | grep dataset.size" > tmp.txt ; tail -1 tmp.txt > pdSize.txt'
        os.system(findPDVolumeCommand) 
        fileInput = open('pdSize.txt', 'r')
        for line in fileInput:
            number = line.rstrip()
            if not number.strip() :
                return 0
            try:
                pdVolume = int(number)
                notFind = False
            except ValueError:
                print "Oops! Got an invalid output for findPDVolume. Let me try again..."
                ncycle += 1
        fileInput.close()
    return pdVolume  

def findDataSetFractions(path, dataset):
    ncycle = 0
    notFind = True
    dataSetSites = [] 
    dataSetFractions = []
    while not exitLoop(ncycle) and  notFind:
        findSitesCommand = 'python ' + path + '/das_client.py --limit=1000 --format=plain --query="site dataset=' + dataset + ' | grep site.name, site.dataset_fraction" | grep _ > tmpSites.txt'
        os.system(findSitesCommand)
        bytes = os.path.getsize('tmpSites.txt')
        if(bytes <= 0):
            return dataSetSites, dataSetFractions
        fileInput = open('tmpSites.txt','r')
        for line in fileInput:
            lineStrip = line.rstrip('\n')
            lineStripSplit = lineStrip.split(' ')
            splitLength = len(lineStripSplit)
            try:
                dataSetFraction = ((lineStripSplit[splitLength - 1].rstrip('"')).rstrip('%')).lstrip('"')
                dataSetFraction = float(dataSetFraction)/100.
                dataSetFractions.append(dataSetFraction)
                frontStrip = lineStripSplit[0].lstrip('[\'"')
                backStrip = frontStrip.rstrip('"\',')
                dataSetSites.append(backStrip)
                notFind = False
            except ValueError:
                print "Oops! Got an invalid output in findDataSetFractions. Let me try again..."
                ncycle += 1
        fileInput.close()
    return dataSetSites, dataSetFractions           

def main():
    
    if(os.path.isfile('./das_client.py') == False):
        print "\n Cannot find das_client.py in this working directory"
        exit()
        
    if(os.path.isfile('./listOfAODs.txt') == False):
        print "\n Cannot find listOfAODs.txt in this working directory"
        exit()

    parser = argparse.ArgumentParser()

    parser.add_argument('--title', default='HI AOD File Set', help="Name for the table title; default is HI AOD File Set")
    parser.add_argument('--nPDs', default=-1, type=int, help="Number of PDs to be processed; default is -1 for all PDs")
    args = parser.parse_args()
    #
    # Get the input parameters from the command line
    #
    title = args.title
    nPDs = args.nPDs
    limitPDs = True
    if(nPDs < 1): limitPDs = False

    x = PrettyTable(["PDs","File Size(GB)", "Files", "#Evts(K)", "# of T2 sites", "First T2", "Second T2", "At VU", "On FNAL Tape"])
    x.align["PD Name"] = "l"
    x.padding_width = 1
    x.float_format = .3;
    x.hrules = ALL
    
    now = datetime.now()
    mm = str(now.month)
    dd = str(now.day)
    yyyy = str(now.year)
    hour = str(now.hour)
    mi = str(now.minute)
    ss = str(now.second)

    tableTitle = title + " Information at %s/%s/%s %s:%s:%s (Nashville time)" % (mm, dd, yyyy, hour, mi, ss)
    print tableTitle
    
    totFiles = 0
    totNEvents = 0 
    totPDVolume = 0 # Byte
    onFNALTapeNumber = 0
    firstT2Number = 0
    secondT2Number = 0
    atVUNumber = 0
 
    fileInput = open("listOfAODs.txt", "r");
    numberOfPDs = 0
    totalNumberOfT2Sites = 0
    volumeOnlyAtVU = 0.0
    volumeAtVanderbilt = 0.0
    volumeAtOtherT2 = 0.0
    volumeAtNoT2 = 0.0
    volumeOnTapeAtFNAL = 0.0
    for dataset in fileInput:
        #
        # Determine the PD name from the input list
        #
        pdNameText = dataset.rstrip('\n')
        pdNameSplit = pdNameText.split(' ')
        if(len(pdNameSplit) > 1):
            pdName = pdNameSplit[1] # special case for the October 2016 list of the HIRun2015 AOD files at Vanderbilt
        else:
            pdName = pdNameText     # usual case for the text files from a DAS query
        numberOfPDs += 1

        listOfSites, listOfFractions = findDataSetFractions(Dir, pdName)
 
        numberOfT2Sites = 0
        onFNALTape = 'No'
        firstT2 = 'None'
        secondT2 = 'None'
        atVU = 'No'
        vuFraction = 0.0
 
        pdVolume = findPDVolume(Dir, pdName)

        for kSite in range(len(listOfSites)):
            siteFullName = listOfSites[kSite]
            siteNameSplit = siteFullName.split('_')

            if(siteNameSplit[0] == 'T2'):
                numberOfT2Sites += 1
                siteName = siteNameSplit[2]
                if(siteNameSplit[2] == 'Vanderbilt'):
                    atVU = 'Yes' + ' (' + str(listOfFractions[kSite]) + ')'
                    atVUNumber += 1
                    siteName = 'VU'
                    vuFraction = listOfFractions[kSite]
                    volumeAtVanderbilt += pdVolume*vuFraction
                else:
                    volumeAtOtherT2 += pdVolume*listOfFractions[kSite]

                if(numberOfT2Sites == 1): firstT2 = siteName + ' (' + str(listOfFractions[kSite]) + ')'; firstT2Number += 1
                if(numberOfT2Sites == 2): secondT2 = siteName + ' (' + str(listOfFractions[kSite]) + ')' ; secondT2Number += 1
     
            if(siteFullName == 'T1_US_FNAL_MSS'):
                onFNALTape = 'Yes' + ' (' + str(listOfFractions[kSite]) + ')'
                onFNALTapeNumber += 1
                volumeOnTapeAtFNAL += pdVolume*listOfFractions[kSite]

        totalNumberOfT2Sites += numberOfT2Sites
        
        if(numberOfT2Sites == 0):
            volumeAtNoT2 += pdVolume

        nEvents = findNEvents(Dir, pdName) 

        nFiles = findNFiles(Dir, pdName)

        if(numberOfT2Sites == 1 and atVU != 'No'):
            volumeOnlyAtVU += pdVolume*vuFraction

        if nEvents < 0 or pdVolume < 0:
            print "Something is wrong! Please check!"

        if nEvents > 0 :
            eventSize = (pdVolume/1.0e6) /nEvents #MB
        else : 
            eventSize = 0      

        totFiles += nFiles
        totNEvents += nEvents
        totPDVolume += pdVolume

        x.add_row([pdName, int(pdVolume/1.0e9), nFiles, int(nEvents/1.0e3), numberOfT2Sites, firstT2, secondT2, atVU, onFNALTape])

        if(limitPDs and numberOfPDs >= nPDs):
            break

    sumText = 'Sum for ' + str(numberOfPDs) + ' PDs'
    averageT2Sites = float(totalNumberOfT2Sites)/float(numberOfPDs)
    averageT2SitesInt = int(100*averageT2Sites)
    averageT2SitesFloat = averageT2SitesInt/100.
    averageT2SitesText = 'Average = ' + str(averageT2SitesFloat)

    x.add_row([sumText, int(totPDVolume/1.0e9), totFiles, int(totNEvents/1.0e3), averageT2SitesText, firstT2Number, secondT2Number, atVUNumber, onFNALTapeNumber])

    print x
    print "\n"

    volumeOnlyAtVUGB = volumeOnlyAtVU/1.0e9
    volumeOnlyAtVUPerCent = 100*volumeOnlyAtVU/totPDVolume
    volumeOnlyAtVUPerCentString = 'GB, corresponding to ' + str(int(volumeOnlyAtVUPerCent+0.5)) + '% of the total PD volume'
    volumeAtVanderbiltGB = volumeAtVanderbilt/1.0e9
    volumeAtOtherT2GB = volumeAtOtherT2/1.0e9
    volumeAtNoT2GB = volumeAtNoT2/1.0e9
    volumeNonUniqueAtVanderbiltT2GB = (totPDVolume - volumeAtNoT2 - volumeOnlyAtVU)/1.0e9
    volumeOnTapeAtFNALGB = volumeOnTapeAtFNAL/1.0e9
    print '%s %d %s' % ('     PD volume amount which exists uniquely at Vanderbilt = ', volumeOnlyAtVUGB, volumeOnlyAtVUPerCentString)
    print '%s %d %s' % ('     PD volume amount total which exists at Vanderbilt = ', volumeAtVanderbiltGB, 'GB')
    print '%s %d %s' % ('     PD volume amount total replicated other T2 sites = ', volumeAtOtherT2GB, 'GB')
    print '%s %d %s' % ('     PD volume amount which exists at no T2 site = ', volumeAtNoT2GB, 'GB')
    print '%s %d %s' % ('     PD volume amount not uniquely at Vanderbilt T2 site = ', volumeNonUniqueAtVanderbiltT2GB, 'GB')
    print '%s %d %s' % ('     PD volume on tape at FNAL = ', volumeOnTapeAtFNALGB, 'GB')
    exit()

if __name__ == '__main__':
    main()

exit()
