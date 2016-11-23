#~/bin/bash

cd ~/tmp/002_S_4213/Resting_State_fMRI/2013-09-17_17_12_40.0/S201576/

mkdir preprocess

dcm2nii -o ./preprocess *.dcm

cd ./preprocess

i=1
while [ $i -le 5 ];
do
    rm *00$i.nii
    i=`expr $i + 1`
    
done

#3dTshift -prefix 0917_base.nii.gz  -tpattern altplus  20130917_171240RestingStatefMRIs601a1006_050.nii

#fslmerge -t 0917_4d.nii *.nii

#3dTshift -prefix 0917_st_F.nii  -tpattern altplus  0917_4d.nii
    
#3dvolreg -prefix 0917_mc_F.nii  -1Dfile _motion.1D  -Fourier -twopass -zpad 4  \
        #-base 0917_base.nii.gz  0917_st_F.nii
    
#3dDespike -prefix 0917_ds_F.nii -ssave _spikiness.nii 0917_mc_F.nii

fslsplit 0917_ds_F.nii 0917_ds_F


## Get functional-to-anatomical image registration

flirt \
 -omat func2anat.mat \
 -cost corratio -dof 12 -interp trilinear \
 -ref ~/tmp/002_S_4213/MPRAGE/2013-09-17_17_12_40.0/S201579/0917_skullstrip.nii\
 -in  0917_ds_F0050.nii\

flirt \
 -omat anat2stnd.mat \
 -cost corratio -dof 12 -interp trilinear \
 -ref ~/tmp/std_skullstrip.nii.gz \
 -in ~/tmp/002_S_4213/MPRAGE/2013-09-17_17_12_40.0/S201579/0917_skullstrip.nii

convert_xfm \
 -omat func2stnd.mat \
 -concat anat2stnd.mat func2anat.mat \
 
# apply MRI to standard registration
flirt -out 0917_MRI.nii -interp trilinear -applyxfm -init anat2stnd.mat \
        -ref ~/tmp/std_skullstrip.nii.gz -in ~/tmp/002_S_4213/MPRAGE/2013-09-17_17_12_40.0/S201579/0917_skullstrip.nii

fsl5.0-fast -o MRI_segm_A -t 1 -n 3 -g -p 0917_MRI.nii

i=0

while [ $i -lt 10 ];
do
    echo $i
    if [ $i -lt 10 ]; then
        fMRI_index=000$i
    elif [ $i -lt 100 ]; then
        fMRI_index=00$i
    else
        fMRI_index=0$i
    fi
    echo $fMRI_index
    
    flirt -out 0917_pp_A_$fMRI_index.nii -interp trilinear -applyxfm -init func2stnd.mat \
        -ref ~/tmp/std_skullstrip.nii.gz -in 0917_ds_F$fMRI_index.nii
    
    
    i=`expr $i + 1`
    
done


fslmerge -t fMRI_registration_4d.nii 0917_pp_A*.nii


3dmaskave \
    -quiet \
    -mask MRI_segm_A_seg_2.nii \
    fMRI_registration_4d.nii > fMRI_csf.1D
    
3dmaskave \
    -quiet \
    -mask MRI_segm_A_seg_0.nii \
    fMRI_registration_4d.nii > fMRI_wm.1D

1dcat fMRI_csf.1D fMRI_wm.1D > fMRI_noise.1D

3dBandpass \
    -prefix fMRI_cl_F.nii \
    -mask 0917_pp_A_0003.nii \
    -ort fMRI_noise.1D \
    0.02 99999 \
    fMRI_registration_4d.nii














   
    

