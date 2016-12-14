#! bin/bash

# This program use for moving data
#
#
#



initial_dataFolder=$1
process_dataFolder=$2

cd $initial_dataFolder

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

    if [ ${arr[0]} == 1 ]; then
        cd /home/medialab/data/$process_dataFolder/$group/$subjectID/
	cd T1
	ls *.nii
    fi
done
