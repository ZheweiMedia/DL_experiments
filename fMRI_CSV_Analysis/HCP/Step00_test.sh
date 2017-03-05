#!/bin/bash

# use for preprocessing data
# usage: bash Step10_preprocessing.sh fMRI_IDs MRI_IDs Philips 3

function processing(){
    fMRI_postFix=$1
    MRI_postFix=$2
    folder_name=$3


    echo $fMRI_postFix

    echo $MRI_postFix

    ### Step 1: preprocessing of T1 images ###
    cd /home/medialab/data/$folder_name/MRI/$MRI_postFix
    
    mv *.nii.gz T1.nii.gz
    gunzip T1.nii.gz

    # remove skull
    3dSkullStrip -o_ply skullstrip_mask.nii -input T1.nii
    3dcalc -prefix skullstrip.nii -expr 'a*step(b)' -b skullstrip_mask.nii -a T1.nii
    ### End of Step 1 ###

    ### Step 2: preprocessing of fMRI images ###
    cd /home/medialab/data/$folder_name/fMRI/$fMRI_postFix
    
    mkdir /home/medialab/data/$folder_name/fMRI/$fMRI_postFix/niiFolder
    cp /home/medialab/data/$folder_name/fMRI/$fMRI_postFix/*.nii.gz \
       /home/medialab/data/$folder_name/fMRI/$fMRI_postFix/niiFolder/fMRI_origin.nii.gz

    rm /home/medialab/data/$folder_name/fMRI/$fMRI_postFix/*

    cd /home/medialab/data/$folder_name/fMRI/$fMRI_postFix/niiFolder
    # discard first 5 images for T1 equilibration effects

    fslsplit fMRI_origin.nii.gz origin

    i=1
    while [ $i -le 5 ];
    do
        rm *00$i.nii
        i=`expr $i + 1`
    done

    fslmerge -t fMRI_4d.nii origin*.nii

    ## slice timing
    3dTshift -prefix slicetiming.nii  -tpattern altplus  fMRI_4d.nii

    ## motion correction
	  3dvolreg -prefix motioncorrection.nii -1Dfile _motion.1D -Fourier -twopass \
             -zpad 4 -base 50 slicetiming.nii

	  ## despike 
	  3dDespike -prefix despike.nii -ssave _spikiness.nii motioncorrection.nii

    ## splite and clean .nii files
	  fslsplit despike.nii despike
	  # rm slicetiming.nii motioncorrection.nii despike.nii fMRI_4d.nii

    ### Step 2: ends ###

    ### Step 3: Get functional-to-standard image registration ###
    # dof set as 6, so now it is rigid registration
	  flirt -omat func2anat.mat -cost corratio -dof 6 -interp trilinear -ref \
          /home/medialab/data/$folder_name/MRI/$MRI_postFix/skullstrip.nii \
          -in despike0050.nii

    despike_fileNo=`ls despike0*.nii | wc`
	  despike_fileNo=($despike_fileNo)
	  despike_fileNo=${despike_fileNo[0]}
	  
	  echo $despike_fileNo

	  ## Apply functional-to-anatimical image registration
	  i=0
	  while [ $i -lt $despike_fileNo ];
	  do
	      if [ $i -lt 10 ]; then
		        fMRI_index=000$i
	      elif [ $i -lt 100 ]; then
		        fMRI_index=00$i
	      else
		        fMRI_index=0$i
	      fi

        # fMRI to T1 space
        flirt -out fMRI_in_MRI_space_$fMRI_index.nii -interp trilinear -applyxfm \
              -init func2anat.mat -ref ~/data/$folder_name/MRI/$MRI_postFix/skullstrip.nii \
              -in despike$fMRI_index.nii
        i=`expr $i + 1`
    done

    

    ## registration of fMRI and std by spm ##
	  python3.5 /home/medialab/Zhewei/fMRI_CSV_Analysis/SIEMENS/utility00_SPM.py \
              /home/medialab/data/$folder_name/MRI/$MRI_postFix/T1.nii \
              fMRI_in_MRI_space_*.nii
    ## registration done ##

    ## remove skull of fMRI
    wfMRI_in_MRI_space_fileNo=`ls wfMRI_in_MRI_space_*.nii | wc`
	  wfMRI_in_MRI_space_fileNo=($wfMRI_in_MRI_space_fileNo)
	  wfMRI_in_MRI_space_fileNo=${wfMRI_in_MRI_space_fileNo[0]}

    echo $wfMRI_in_MRI_space_fileNo

	  i=0
	  while [ $i -lt $wfMRI_in_MRI_space_fileNo ];
	  do
	      if [ $i -lt 10 ]; then
		        fMRI_index=000$i
	      elif [ $i -lt 100 ]; then
		        fMRI_index=00$i
	      else
		        fMRI_index=0$i
	      fi
        fslmaths wfMRI_in_MRI_space_$fMRI_index.nii\
                 -mas ~/data/template/MNI152_T1_2mm_brain_mask.nii.gz \
                 _fMRI_brain_$fMRI_index.nii
        i=`expr $i + 1`
	  done
    ## remove skull of fMRI done

    fslmerge -t registration_fMRI_4d.nii _fMRI_brain_*.nii
    
    ### Step 3: ends ###

    ### Step 4: Remove noise signal ###

    ## remove skull of MRI
    mv /home/medialab/data/$folder_name/MRI/$MRI_postFix/wT1.nii .

    fslmaths wT1.nii \
             -mas ~/data/template/MNI152_T1_2mm_brain_mask.nii.gz \
             registration_T1.nii
    
	  ## segment anatomical image
	  fsl5.0-fast -o T1_segm_A -t 1 -n 3 -g -p registration_T1.nii

    ## Get mean signal of CSF segment
	  3dmaskave -quiet -mask T1_segm_A_seg_0.nii registration_fMRI_4d.nii > fMRI_csf.1D

    ## motion correction in the standard space
	  3dvolreg -prefix _mc_F.nii -1Dfile fMRI_motion.1D -Fourier -twopass \
             -zpad 4 -base 50 registration_fMRI_4d.nii

	  ## Get motion derivative
	  1d_tool.py -write fMRI_motion_deriv.1D -derivative -infile fMRI_motion.1D

	  ## concatenate CSF signal, motion correction, motion derivative into 'noise signal'
	  1dcat fMRI_csf.1D fMRI_motion.1D fMRI_motion_deriv.1D > fMRI_noise.1D

	  ## Regress out the 'noise signal' from functional image
	  3dBandpass -prefix fMRI_removenoise_Bandpass.nii -mask _fMRI_brain_0003.nii \
               -ort fMRI_noise.1D 0.02 0.1 registration_fMRI_4d.nii

    3dBandpass -prefix fMRI_removenoise_Highpass.nii -mask _fMRI_brain_0003.nii \
               -ort fMRI_noise.1D 0.02 99999 registration_fMRI_4d.nii

    ## Generate modified AAL2 corresponding to fMRI
    3dAutomask -prefix fMRI_mask.nii _fMRI_brain_0003.nii
    fslmaths ~/data/template/AAL2_after_stdmask.nii -mas fMRI_mask.nii AAL2_for_fMRI.nii

    ## final results
    mkdir /home/medialab/data/$folder_name/fMRI/$fMRI_postFix/Bandpass
    
    mkdir /home/medialab/data/$folder_name/fMRI/$fMRI_postFix/Highpass

    mkdir /home/medialab/data/$folder_name/fMRI/$fMRI_postFix/Original

    i=1
    cat ~/data/template/ROI_index.txt | while read line;do
        roi_value=$(echo $line | tr -d '\r')

        3dmaskave \
            -quiet \
            -mrange $(echo $roi_value-0.1 | bc) $(echo $roi_value+0.1 | bc) \
            -mask AAL2_for_fMRI.nii \
            fMRI_removenoise_Bandpass.nii > /home/medialab/data/$folder_name/fMRI/$fMRI_postFix/Bandpass/_t${i}.1D

        i=`expr $i + 1`
    done

    i=1
    cat ~/data/template/ROI_index.txt | while read line;do
        roi_value=$(echo $line | tr -d '\r')

        3dmaskave \
            -quiet \
            -mrange $(echo $roi_value-0.1 | bc) $(echo $roi_value+0.1 | bc) \
            -mask AAL2_for_fMRI.nii \
            fMRI_removenoise_Highpass.nii > /home/medialab/data/$folder_name/fMRI/$fMRI_postFix/Highpass/_t${i}.1D

        i=`expr $i + 1`
    done

    i=1
    cat ~/data/template/ROI_index.txt | while read line;do
        roi_value=$(echo $line | tr -d '\r')

        3dmaskave \
            -quiet \
            -mrange $(echo $roi_value-0.1 | bc) $(echo $roi_value+0.1 | bc) \
            -mask AAL2_for_fMRI.nii \
            registration_fMRI_4d.nii > /home/medialab/data/$folder_name/fMRI/$fMRI_postFix/Original/_t${i}.1D

        i=`expr $i + 1`
    done

    niifiles=`ls *.nii`
    for nii in ${niifiles[@]};
    do
        gzip $nii
    done

    
    }





fMRI_imageIDs=(`cat $1`)
MRI_imageIDs=(`cat $2`)
folder_name=$3


Core=6
ID_Number=$4
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
