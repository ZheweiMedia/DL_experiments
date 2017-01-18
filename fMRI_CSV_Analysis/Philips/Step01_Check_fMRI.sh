#!/bin/bash

# This bash script do dcm2nii, then copy one time frame to a fold fMRI_check


# go to the fold contain the files

cd /home/medialab/data/ADNI/ADNI

# read all fMRI .xml files
XMLS=`find ./ -name "*Resting_State_fMRI*.xml"`

mkdir /home/medialab/data/ADNI/fMRI_check

Used_core=6
(
for X in $XMLS;
do
    ((i=i%Used_core)); ((i++==0)) && wait

    (iid=`xmllint --xpath '//project/subject/study/series/imagingProtocol/imageUID/text()' $X`
    time=`xmllint --xpath '//project/subject/study/series/dateAcquired/text()' $X`

    # string of time in files
    timeYear=${time:0:4}
    timeMonthDay=${time:5:5}
    timeMonth=${timeMonthDay:0:2}
    timeDay=${timeMonthDay:3:4}
    timeFilt=$timeYear$timeMonth$timeDay

    # find all dcm file of one iid
    dcm_fMRI=`find $PWD -name "*Resting_State_fMRI*${iid}*.dcm"`
    # copy all dcm to fMRI_preprocess
    mkdir /home/medialab/data/ADNI/fMRI_${iid}
    cp $dcm_fMRI /home/medialab/data/ADNI/fMRI_${iid}
    dcm2nii -g n -n y /home/medialab/data/ADNI/fMRI_${iid}
    cp /home/medialab/data/ADNI/fMRI_${iid}/*$timeFile*_*_100.nii /home/medialab/data/ADNI/fMRI_check/fMRI_${iid}.nii
    rm -r /home/medialab/data/ADNI/fMRI_${iid}) &
done
)
