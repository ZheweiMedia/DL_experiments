#!/bin/bash

# in python, output the image id to a file named by the DX_Group.
# Then read this file to this bash script.
# This bash script do dcm2nii, then copy one time frame to a fold fMRI_Check.

Scan_all_folder () {
# go to the fold which contain the files

cd /home/medialab/data/ADNI/ADNI
# list the samples we want to process
# IIDarray is the parameter passed by command line,
# $0 is the name of command, $1is the parameter
IIDarray=$1
# read all samples
XMLS=`find ./ -name "*Resting_State_fMRI*.xml"`

declare -i fileShould=140
mkdir /home/medialab/data/ADNI/fMRI_check

# compare them
for X in $XMLS
do
    iid=`xmllint --xpath '//project/subject/study/series/imagingProtocol/imageUID/text()' $X`
    time=`xmllint --xpath '//project/subject/study/series/dateAcquired/text()' $X`
    # echo $iid
    # find out the correct time for .nii time. Because after dcm2nii, sometimes we have more
    # than 140 nii files for one subject.
    timeYear=${time:0:4}
    timeMonthDay=${time:5:5}
    timeMonth=${timeMonthDay:0:2}
    timeDay=${timeMonthDay:3:4}
    timeFilt=$timeYear$timeMonth$timeDay
    
    # echo $timeFilt
    No=$fileShould
    case "${IIDarray[@]}" in  *$iid*)
        # find sid to identify .dcm files
        # sid=`xmllint --xpath '//project/subject/subjectIdentifier/text()' $X`
        # find the path to .dcm
        dcm_fMRI=`find $PWD -name "*Resting_State_fMRI*${iid}*.dcm"`
        # cp .dcm to new fold, then dcm2nii, then delete .dcm in the new fold
        mkdir /home/medialab/data/ADNI/fMRI_${iid}
        cp $dcm_fMRI /home/medialab/data/ADNI/fMRI_${iid}
        dcm2nii  -g n -n y /home/medialab/data/ADNI/fMRI_${iid}
        del_dcmFile=`find /home/medialab/data/ADNI/fMRI_${iid}/ -name "*.dcm"`
        rm $del_dcmFile
        # find all .nii file, and output the full path to a .txt file
        # here should use some filt to remove the .nii files that not belongs to
        # the 140 niis.
        nii_file=`find /home/medialab/data/ADNI/fMRI_${iid}/  -name "*$timeFilt*_*_*.nii"`
        No=0
        for nii in $nii_file
        do
            readlink -f $nii >> fMRI_${iid}.txt
            No=`expr $No + 1`
        done
	cp /home/medialab/data/ADNI/fMRI_${iid}/*$timeFilt*_*_100.nii /home/medialab/data/ADNI/fMRI_check/fMRI_${iid}.nii
    esac
    if [ $No -ne $fileShould ]
    then
        echo $iid
        echo $iid >> fMRI_Fail.txt
    fi
    # echo $No # check how many files
done
}
Scan_all_folder
