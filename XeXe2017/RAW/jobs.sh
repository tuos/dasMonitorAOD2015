#!/bin/bash

source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc6_amd64_gcc530
export SSL_CERT_DIR=/etc/grid-security/certificates

cd /home/tuos/run2016/dasDataVolume/CMSSW_8_0_22/src/charlieScipt/RAW
eval `scramv1 runtime -sh`
dateAndTime=$(date +"%Y%m%d_%H%M%S")
filename="outputPrintRAW_$dateAndTime.txt"
python printHIRAWSites.py > "$filename"

#dateAndTime=$(date +"%Y%m%d_%H%M%S")
#filename="vandySize_$dateAndTime.txt"
#/usr/local/lio/bin/lio_du -h -s @:/cms/store/hidata/XeXeRun2017/ > "$filename"
#cd /home/tuos/run2016/dasDataVolume/CMSSW_8_0_22/src/charlieScipt/RAW
#cp vandySize_* /home/tuos/web/run2017/


