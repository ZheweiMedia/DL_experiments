#!/bin/bash

# After SPM, the links of each fMRI files are changed because the last step of
# SPM: spatial normalization has a prefix 'w' and cannot set it as none.
# So after SPM, we need to scan the folds and output the links again


# go to the fold of .xml which contain the files

cd /home/medialab/data/ADNI/ADNI
# list the samples we want to process
# IIDarray is the parameter passed by command line,
# $0 is the name of command, $1 is the parameter

IIDarray=`cat ~/Zhewei/fMRI_SubjectAnalysis/$1`
echo $IIDarray
# read all samples
XMLS=`find ./ -name "*Resting_State_fMRI*.xml"`

declare -i fileShould=130
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
	echo $iid
        
        # find all .nii file, and output the full path to a .txt file
        # here should use some filt to remove the .nii files that not belongs to
        # the 140 niis.
	
        nii_file=`find /home/medialab/data/ADNI/fMRI_${iid}/  -name "w$timeFilt*_*_*.nii"`
        No=0
        for nii in $nii_file
        do
            readlink -f $nii >> fMRI_SPM_${iid}.txt
            No=`expr $No + 1`
        done
    esac
    if [ $No -ne $fileShould ]
    then
        echo $iid
        echo $iid >> fMRI_Fail.txt
    fi
    # echo $No # check how many files
done
