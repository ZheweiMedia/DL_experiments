#!/bin/bash

# we should have 282 fMRI images. In fMRI_check fold we only have 279.
# Find out what happened.


cd /home/medialab/data/ADNI/fMRI_check

fMRI_check_ID=`ls `

cd /home/medialab/data/ADNI/ADNI
XMLS=`find ./ -name "*Resting_State_fMRI*.xml"`

for X in $XMLS;
do
    iid=`xmllint --xpath '//project/subject/study/series/imagingProtocol/imageUID/text()' $X`
    fMRI_file_name=fMRI_$iid.nii
    case "$fMRI_check_ID[@]"  in
        *$fMRI_file_name*)
            :;;
        *)
            echo $fMRI_file_name;;
    esac
 done
