#!/bin/bash

# use for preprocessing data
# usage: bash Step10_preprocessing.sh fMRI_IDs MRI_IDs Philips 3

function processing(){

    fMRI_ID=$1

    cd /media/medialab/Seagate\ Expansion\ Drive/ADNI/SIEMENS/fMRI/*$fMRI_ID*/niiFolder/ 

    

    ## final results
    mkdir /home/medialab/Zhewei/fMRI_CSV_Analysis/smallDataset/MRI_results/$fMRI_ID
    echo $fMI_ID
    i=1
    cat ~/data/template/ROI_index.txt | while read line;do
        roi_value=$(echo $line | tr -d '\r')

        3dmaskave \
            -quiet \
            -mrange $(echo $roi_value-0.1 | bc) $(echo $roi_value+0.1 | bc) \
            -mask ~/data/template/AAL2_after_stdmask.nii \
            ./registration_T1.nii \
            > /home/medialab/Zhewei/fMRI_CSV_Analysis/smallDataset/MRI_results/$fMRI_ID/_t${i}.1D

        i=`expr $i + 1`
    done
    
    }





fMRI_imageIDs=(`cat $1`)

Core=6
# ID_number = 234
ID_Number=$2
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
    processing ${fMRI_imageIDs[i]} & 
done
