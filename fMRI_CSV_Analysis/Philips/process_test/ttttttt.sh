#!/bin/bash

# use for preprocessing data

function processing(){
    fMRI_postFix=$1
    MRI_postFix=$2

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
    cd /home/medialab/data/ADNI/process_test/MRI/$MRI_postFix
    dcm2nii -g n -n y /home/medialab/data/ADNI/process_test/MRI/$MRI_postFix

    # clean folder
    rm *.dcm
    keywords=^$MRI_timeStamp
    ls | grep -v $keywords |xargs rm
    echo `ls *`
    mv *.nii T1.nii
    
}





fMRI_imageIDs=(`cat $1`)
MRI_imageIDs=(`cat $2`)


Core=2
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
    processing ${fMRI_imageIDs[i]} ${MRI_imageIDs[i]}& 
done
