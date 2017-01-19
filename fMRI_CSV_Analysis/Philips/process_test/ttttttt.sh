#!/bin/bash

# use for preprocessing data

function processing(){
    fMRI_postFix=$1
    MRI_postFix=$2
    folder_name=$3

    fMRI_ID=${fMRI_postFix:5:6}
    fMRI_timeStamp=${fMRI_postFix:12:19}

    MRI_ID=${MRI_postFix:4:6}
    MRI_timeStamp=${MRI_postFix:11:18}

    echo $fMRI_postFix
    echo $fMRI_ID
    echo $fMRI_timeStamp

    echo $MRI_postFix
    echo $MRI_ID
    echo $MRI_timeStamp

    ### Step 1: preprocessing of T1 images ###
    cd /home/medialab/data/ADNI/$folder_name/MRI/$MRI_postFix
    dcm2nii -g n -n y /home/medialab/data/ADNI/$folder_name/MRI/$MRI_postFix

    # clean folder
    rm *.dcm
    keywords=^$MRI_timeStamp
    ls | grep -v $keywords |xargs rm
    echo `ls *`
    mv *.nii T1.nii

    # remove skull
    3dSkullStrip -o_ply skullstrip_mask.nii -input T1.nii
    3dcalc -prefix skullstrip.nii -expr 'a*step(b)' -b skullstrip_mask.nii -a T1.nii
    ### End of Step 1 ###

    ### Step 2: preprocessing of fMRI images ###
    cd /home/medialab/data/ADNI/$folder_name/fMRI/$fMRI_postFix
    dcm2nii -g n -n y /home/medialab/data/ADNI/$folder_name/fMRI/$fMRI_postFix
    mkdir /home/medialab/data/ADNI/$folder_name/fMRI/$fMRI_postFix/niiFolder
    cp /home/medialab/data/ADNI/$folder_name/fMRI/$fMRI_postFix/*$fMRI_timeStamp*_*_*.nii \
       /home/medialab/data/ADNI/$folder_name/fMRI/$fMRI_postFix/niiFolder
    rm /home/medialab/data/ADNI/$folder_name/fMRI/$fMRI_postFix/*
    
}





fMRI_imageIDs=(`cat $1`)
MRI_imageIDs=(`cat $2`)
folder_name=$3


Core=3
ID_Number=5
range_array=()

for ((i=0; $i<ID_Number; i++));
do
    echo $i
    range_array+=($i)
done
echo ${range_array[@]}
for i in ${range_array[@]};
do
    ((c=c%Core)); ((c++==0)) && wait
    echo $i
    processing ${fMRI_imageIDs[i]} ${MRI_imageIDs[i]} $folder_name& 
done




