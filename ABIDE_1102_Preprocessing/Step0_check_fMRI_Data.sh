#! /bin/bash

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# This step is omitted.
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# This program use to check ABIDE fMRI data
#
# Usage: bash check_fMRI_Data path/to/dataFolder
#
# one volume of fMRI data will be copied to ~/data/ABIDE_Check_fMRI
#
# After running this program, freeview ~/data/ABIDE_Check_fMRI/*.nii to check
# bad data.

initialdir=`pwd`

dataFolder=$1

cd /home/medialab/data/
mkdir ./ABIDE_Check_fMRI
mkdir ./ABIDE_Check_fMRI/full_data

rm -r ./ABIDE_Check_fMRI/*.nii
rm -r ./ABIDE_Check_fMRI/full_data/*

cd $dataFolder
echo $dataFolder

# read all .xml file, separate as ABIDE or Control

xmlfiles=`ls *Resting_State_fMRI*.xml`

for xmlfile in $xmlfiles; do
    echo ''
    echo xmlfile: $xmlfile

    subjectID=`xmllint --xpath '//project/subject/subjectIdentifier/text()' $xmlfile`
    echo $subjectID
    fMRI_fileNo=`ls ./$subjectID/Resting_State_fMRI/*/ | wc`
    arr=($fMRI_fileNo)
    
    if [ ${arr[0]} != 1 ]; then
        echo ${arr[0]}
        echo $subjectID >> /home/medialab/data/ABIDE_Check_fMRI/Error_subjectID.txt
    else
        cp ./$subjectID/Resting_State_fMRI/*/*/*.nii /home/medialab/data/ABIDE_Check_fMRI/full_data
        cd /home/medialab/data/ABIDE_Check_fMRI/full_data
        fslsplit *.nii fMRI_
        mv fMRI_0050.nii ../$subjectID.nii
        rm ./*.nii
        cd /home/medialab/data/$dataFolder
    fi
    
done
