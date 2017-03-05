#!/bin/bash

# move all HCP-Q1 data to processing folder.
#
#
#
#


subjects_list=(`cat $1`)

for subjects in ${subjects_list[@]};
do
    echo $subjects
    mkdir ~/data/HCP-Q1/fMRI/$subjects
    cp /media/medialab/HCP-Q1/$subjects/unprocessed/3T/tfMRI_EMOTION_LR/${subjects}_3T_tfMRI_EMOTION_LR.nii.gz ~/data/HCP-Q1/fMRI/$subjects/

    mkdir ~/data/HCP-Q1/MRI/$subjects
    cp /media/medialab/HCP-Q1/$subjects/unprocessed/3T/T1w_MPR1/${subjects}_3T_T1w_MPR1.nii.gz ~/data/HCP-Q1/MRI/$subjects
done


