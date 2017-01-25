#!/bin/bash

# This bash script do dcm2nii, then copy one time frame to a fold fMRI_check


# go to the fold contain the files

cd /home/medialab/data/ADNI/SIEMENS/ADNI

# read all fMRI .xml files
XMLS=`find ./ -name "*MoCoSeries*.xml"`

mkdir /home/medialab/data/ADNI/SIEMENS/fMRI_check

total_nii=105

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
    echo $timeYear
    echo $timeFilt
    echo $iid

    # find all dcm file of one iid
    dcm_fMRI=`find $PWD -name "*MoCoSeries*${iid}*.dcm"`
    # copy all dcm to fMRI_preprocess
    mkdir /home/medialab/data/ADNI/SIEMENS/fMRI_${iid}
    cp $dcm_fMRI /home/medialab/data/ADNI/SIEMENS/fMRI_${iid}
    dcm2nii -g n -n y /home/medialab/data/ADNI/SIEMENS/fMRI_${iid}
    nii_number=`ls /home/medialab/data/ADNI/SIEMENS/fMRI_${iid}/*$timeFilt*_*_*.nii | wc -l`
    echo $nii_number
    if [ $nii_number -ne $total_nii ]
    then
        echo $iid >> /home/medialab/data/ADNI/SIEMENS/fMRI_Fail.txt
        echo $timeFile >> /home/medialab/data/ADNI/SIEMENS/fMRI_Fail.txt
        echo $nii_number >> /home/medialab/data/ADNI/SIEMENS/fMRI_Fail.txt
        echo `ls /home/medialab/data/ADNI/SIEMENS/fMRI_${iid}/*$timeFilt*_*_*.nii` >> /home/medialab/data/ADNI/SIEMENS/fMRI_Fail.txt
    fi

    cp /home/medialab/data/ADNI/SIEMENS/fMRI_${iid}/*$timeFilt*_*_050.nii /home/medialab/data/ADNI/SIEMENS/fMRI_check/fMRI_${iid}.nii
    rm -r /home/medialab/data/ADNI/SIEMENS/fMRI_${iid}) &
done
)
