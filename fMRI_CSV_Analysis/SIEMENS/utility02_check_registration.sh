#!/bin/bash


fMRI_imageIDs=(`cat $1`)
MRI_imageIDs=(`cat $2`)
folder_name=$3

mkdir ~/data/ADNI/$folder_name/check_registration/

for i in ${fMRI_imageIDs[@]};
do
    cp ~/data/ADNI/$folder_name/fMRI/$i/niiFolder/wdespike0058.nii \
       ~/data/ADNI/$folder_name/check_registration/$i.nii
done

