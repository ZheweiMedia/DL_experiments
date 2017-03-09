#!/bin/bash

# set the check_registration folder

mkdir ~/data/HCP-Q1/$1

folders_name=`cat $2`

for folder in ${folders_name[@]};
do
    cp ~/data/HCP-Q1/fMRI/$folder/niiFolder/wfMRI_in_MRI_space_0100.nii.gz ~/data/HCP-Q1/$1/$folder.nii.gz
done

