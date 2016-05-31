#!/bin/bash


# cat the result of MatLab belongs to the same subject to a file 

# change line 27 for different groups


cd /home/medialab/data/ADNI/ADNI
# list the samples we want to process
IIDarray=( 346237 248516 258600 287986 322000 \
375331 360323 301395 306073 360317 \
382187 258955 280778 300334 343912 \
345555 228872 357475 376933 368413 \
291229 295969 300043 306375 342326 \
341793 342278 342915 347402 348491 \
358777 381307 367567 342514)

XMLS=`find ./ -name "*Resting_State_fMRI*.xml"`

for X in $XMLS
do
    iid=`xmllint --xpath '//project/subject/study/series/imagingProtocol/imageUID/text()' $X`
    subj=`xmllint --xpath '//project/subject/subjectIdentifier/text()' $X`
    case "${IIDarray[@]}" in  *$iid*)
        echo $iid
        cat /home/medialab/Zhewei/data/AD_Results/AD_Result${iid}.txt >> /home/medialab/Zhewei/data/AD_Results/AD_Subj${subj}_Baseline
    esac
done
