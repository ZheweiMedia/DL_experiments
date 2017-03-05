#!/bin/bash

cd ~/data/HCP-Q1/test_HCP-Q1/fMRI/255639/niiFolder

niifiles=`ls *.nii`

for nii in ${niifiles[@]};
do
    gzip $nii
done

