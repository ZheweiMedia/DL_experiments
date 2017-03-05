#!/bin/bash



mkdir ~/data/HCP-Q1/check_registration/

folders_name=`cat $1`

for folder in ${folders_name[@]};
do
    cp ~/data/HCP-Q1/fMRI/$folder/niiFolder/wfMRI_in_MRI_space_0100.nii.gz ~/data/HCP-Q1/check_registration/$folder.nii.gz
done

