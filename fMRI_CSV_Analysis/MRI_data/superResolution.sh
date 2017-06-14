#!/bin/bash

# use for preprocessing data
# usage: bash Step10_preprocessing.sh fMRI_IDs MRI_IDs Philips 3

function processing(){
    
    MRI_15ID=$1
    MRI_30ID=$2
    

    ### Step 1: preprocessing of 15 images ###
    cd /home/medialab/data/SuperResolution/Experiment/$MRI_15ID
    dcm2nii -g n -n y /home/medialab/data/SuperResolution/Experiment/$MRI_15ID/

    # clean folder
    rm *.dcm
    mv 2*.nii 15T1.nii
    
    ### End of Step 1 ###

    ### Step 2: preprocessing of 30 images ###
    cd /home/medialab/data/SuperResolution/Experiment/$MRI_30ID
    dcm2nii -g n -n y /home/medialab/data/SuperResolution/Experiment/$MRI_30ID/

    # clean folder
    rm *.dcm
    mv 2*.nii 30T1.nii
    
    ### End of Step 1 ###

    ### Step 3: Get 15 img and 30 img registration ###
    mv /home/medialab/data/SuperResolution/Experiment/$MRI_15ID/15T1.nii \
       /home/medialab/data/SuperResolution/Experiment/$MRI_30ID/
    ## registration of fMRI and std by spm ##
	  python3.5 /home/medialab/Zhewei/fMRI_CSV_Analysis/MRI_data/utility01_SPM_coregistration.py \
              /home/medialab/data/SuperResolution/Experiment/$MRI_30ID/30T1.nii \
              /home/medialab/data/SuperResolution/Experiment/$MRI_30ID/15T1.nii
    ## registration done ##

    ### Step 4: Remove skull of MRI ###
    # Now 15T1.nii is r15T1.nii
    ## remove skull of MRI
    cd /home/medialab/data/SuperResolution/Experiment/$MRI_30ID
    3dSkullStrip -o_ply skullstrip_mask.nii -input 30T1.nii
    3dcalc -prefix skullstrip30.nii -expr 'a*step(b)' -b skullstrip_mask.nii -a 30T1.nii
    3dcalc -prefix skullstrip15.nii -expr 'a*step(b)' -b skullstrip_mask.nii -a r15T1.nii

    
    }






MRI_imageID15=(`cat $1`)
MRI_imageID30=(`cat $2`)

Core=6
# ID_Number=521
ID_Number=$3
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
    processing ${MRI_imageID15[i]} ${MRI_imageID30[i]} & 
done
