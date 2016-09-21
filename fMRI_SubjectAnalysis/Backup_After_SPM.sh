#!/bin/bash

# For each subject, SPM processing cost about 14 mins. So after SPM, we should backup all data. Play safe.


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

	cp -r /home/medialab/data/ADNI/fMRI_${iid} /home/medialab/data/Backup_ADNI/Backup_ADNI_After_SPM/
        
    esac
done
