#!/bin/bash

# After SPM processing, generate the files that have a prefix 'w'.
# Copy one time steps of fMRI files to a fold.
#
# Zhewei @9/20/2016

cd /home/medialab/data/ADNI/ADNI

# list the samples we want to process
# IIDarray is the parameter passed by command line,
# $0 is the name of command, $1 is the parameter

IIDarray=`cat ~/Zhewei/fMRI_SubjectAnalysis/$1`
echo $IIDarray
# read all samples
XMLS=`find ./ -name "*Resting_State_fMRI*.xml"`
declare -i fileShould=1

mkdir /home/medialab/data/ADNI/MRI_check

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
    echo $iid
    No=$fileShould
    case "${IIDarray[@]}" in  *$iid*)
	# nii_file=`find /home/medialab/data/ADNI/fRI_${iid}/  -name "w$timeFilt*.nii"`
	echo w$timeFilt
	cp /home/medialab/data/ADNI/fMRI_${iid}/w$timeFilt*_100.nii /home/medialab/data/ADNI/fMRI_check/fMRI_${iid}.nii
    esac
    # echo $No # check how many files
done
