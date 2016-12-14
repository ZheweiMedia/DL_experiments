#! bin/bash

# This program use for moving data
#
#
#





initialdir=`pwd`

dataFolder=$1

cd /home/medialab/data/
mkdir ./ABIDE_Data_Process
rm -r ./ABIDE_Data_Process/*
mkdir ./ABIDE_Data_Process/Autism
mkdir ./ABIDE_Data_Process/Control

cd $dataFolder

# read all .xml file, separate as ABIDE or Control

xmlfiles=`ls *Resting_State_fMRI*.xml`

for xmlfile in $xmlfiles; do
    echo ''
    echo xmlfile: $xmlfile

    subjectID=`xmllint --xpath '//project/subject/subjectIdentifier/text()' $xmlfile`
    group=`xmllint --xpath '//project/subject/researchGroup/text()' $xmlfile`
    echo $subjectID
    
    fMRI_fileNo=`ls ./$subjectID/Resting_State_fMRI/*/ | wc`
    arr=($fMRI_fileNo)
    
    if [ ${arr[0]} != 1 ]; then
        echo $subjectID >> /home/medialab/data/ABIDE_Data_Process/Error_subjectID.txt
    else
        mkdir /home/medialab/data/ABIDE_Data_Process/$group/$subjectID
        mkdir /home/medialab/data/ABIDE_Data_Process/$group/$subjectID/T1
        mkdir /home/medialab/data/ABIDE_Data_Process/$group/$subjectID/fMRI
        cp ./$subjectID/Resting_State_fMRI/*/*/*.nii  /home/medialab/data/ABIDE_Data_Process/$group/$subjectID/fMRI
        cp ./$subjectID/MP-RAGE/*/*/*.nii  /home/medialab/data/ABIDE_Data_Process/$group/$subjectID/T1
        
    fi
    
done
