#!/bin/bash

# use for preprocessing data
# usage: bash Step10_preprocessing.sh fMRI_IDs MRI_IDs Philips sample_numbers

function processing(){

    MRI_ID=$1
    
    ### Step 1: preprocessing of T1 images ###
    cd /home/medialab/data/ALL_MRI_Data/$MRI_ID
    dcm2nii -g n -n y /home/medialab/data/ALL_MRI_Data/$MRI_ID

    # clean folder
    rm *.dcm
    mv 2*.nii T1.nii

    # remove skull
    3dSkullStrip -o_ply skullstrip_mask.nii -input T1.nii
    3dcalc -prefix skullstrip.nii -expr 'a*step(b)' -b skullstrip_mask.nii -a T1.nii
    ### End of Step 1 ###

    

    # Get anatimical-to-standard image registration
	  flirt -omat anat2stnd.mat -cost corratio -dof 12 -interp trilinear -ref \
          ~/data/template/std_skullstrip.nii.gz -in \
          /home/medialab/data/ALL_MRI_Data/$MRI_ID/skullstrip.nii

    # apply MRI to standard registration
	  flirt -out registration_T1.nii -interp trilinear -applyxfm -init anat2stnd.mat \
          -ref ~/data/template/std_skullstrip.nii.gz -in \
          /home/medialab/data/ALL_MRI_Data/$MRI_ID/skullstrip.nii

    
	  
    mkdir /home/medialab/Zhewei/fMRI_CSV_Analysis/MRI_data/MRI_results/$MRI_ID
    i=1
    cat ~/data/template/ROI_index.txt | while read line;do
        roi_value=$(echo $line | tr -d '\r')

        3dmaskave \
            -quiet \
            -mrange $(echo $roi_value-0.1 | bc) $(echo $roi_value+0.1 | bc) \
            -mask ~/data/template/AAL2.nii \
            /home/medialab/data/ALL_MRI_Data/$MRI_ID/registration_T1.nii > /home/medialab/Zhewei/fMRI_CSV_Analysis/MRI_data/MRI_results/$MRI_ID/_t${i}.1D

        i=`expr $i + 1`
    done    
    }





MRI_imageIDs=(`cat $1`)


Core=2

#ID_Number=515
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
    processing ${MRI_imageIDs[i]}& 
done
