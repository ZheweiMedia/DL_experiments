#!/bin/bash

# use for preprocessing data
# usage: bash Step10_preprocessing.sh fMRI_IDs MRI_IDs Philips 3

function processing(){
    
    MRI_ID=$1
    

    ### Step 1: preprocessing of T1 images ###
    cd /home/medialab/data/ALL_MRI_Data/$MRI_ID
    dcm2nii -g n -n y /home/medialab/data/ALL_MRI_Data/$MRI_ID

    # clean folder
    rm *.dcm
    mv 2*.nii T1.nii
    
    ### End of Step 1 ###

    ### Step 3: Get functional-to-standard image registration ###

    ## registration of fMRI and std by spm ##
	  python3.5 /home/medialab/Zhewei/fMRI_CSV_Analysis/MRI_data/utility00_SPM.py \
              /home/medialab/data/ALL_MRI_Data/$MRI_ID/T1.nii
    ## registration done ##

    ### Step 4: Remove noise signal ###

    ## remove skull of MRI

    fslmaths wT1.nii \
             -mas ~/data/template/MNI152_T1_2mm_brain_mask.nii.gz \
             registration_T1.nii
    

    ## Generate modified AAL2 corresponding to MRI
    3dAutomask -prefix MRI_mask.nii registration_T1.nii
    fslmaths ~/data/template/AAL2_after_stdmask.nii -mas MRI_mask.nii AAL2_for_MRI.nii

    ## final results
    mkdir /home/medialab/Zhewei/fMRI_CSV_Analysis/MRI_data/MRI_results/$MRI_ID

    i=1
    cat ~/data/template/ROI_index.txt | while read line;do
        roi_value=$(echo $line | tr -d '\r')

        3dmaskave \
            -quiet \
            -mrange $(echo $roi_value-0.1 | bc) $(echo $roi_value+0.1 | bc) \
            -mask AAL2_for_MRI.nii \
            /home/medialab/data/ALL_MRI_Data/$MRI_ID/registration_T1.nii \
            > /home/medialab/Zhewei/fMRI_CSV_Analysis/MRI_data/MRI_results/$MRI_ID/_t${i}.1D

        i=`expr $i + 1`
    done

    
    }






MRI_imageIDs=(`cat $1`)


Core=6
# ID_Number=515
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
