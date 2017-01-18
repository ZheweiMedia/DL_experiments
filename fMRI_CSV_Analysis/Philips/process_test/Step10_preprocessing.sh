#!/bin/bash

# use for preprocessing data

fMRI_imageIDs=(`cat $1`)
MRI_imageIDs=(`cat $2`)


ID_Number=5
for ((i=0; $i<ID_Number; i++))
do
    echo $i
    echo ${fMRI_imageIDs[i]}
done




function processing(){
    fMRI_postFix=$1
    MRI_ID=$2

    fMRI_ID=${fMRI_postFix:5:10}
    fMRI_timeStamp=${fMRI_postFix:12:19}

    ### Step 1: preprocessing of T1 images ###
    cd /home/medialab/data/ADNI/process_test/MRI/MRI_$MRI_ID
    dcm2nii -g n -n y .
    rm *.dcm co*.nii o*.nii
    mv *.nii T1.nii
    # remove skull
    3dSkullStrip -o_ply skullstrip_mask.nii -input T1.nii
    3dcalc -prefix skullstrip.nii -expr 'a*step(b)' -b skullstrip_mask.nii -a T1.nii
    ### End of Step 1 ###


    ### Step 2: preprocessing of fMRI images ###
    cd /home/medialab/data/ADNI/process_test/fMRI/fMRI_$fMRI_postFix
    dcm2nii -g n -n y .
    mkdir ./niiFolder
    cp ./*$fMRI_timeStamp*_*_*.nii ./niiFolder
    rm *

    cd ./niiFolder
    # discard first 5 images for T1 equilibration effects
    i=1
    while [ $i -le 5 ];
    do
        rm *00$i.nii
        i=`expr $i + 1`
    done

    fslmerge -t fMRI_4d.nii *.nii
    rm *$fMRI_timeStamp*_*_*.nii

    ## slice timing
    3dTshift -prefix slicetiming.nii  -tpattern altplus  fMRI_4d.nii

    ## motion correction
	  3dvolreg -prefix motioncorrection.nii -1Dfile _motion.1D -Fourier -twopass \
             -zpad 4 -base 50 slicetiming.nii

	  ## despike 
	  3dDespike -prefix despike.nii -ssave _spikiness.nii motioncorrection.nii

    ## splite and clean .nii files
	  fslsplit despike.nii despike
	  rm slicetiming.nii motioncorrection.nii despike.nii fMRI_4d.nii

    ### Step 2: ends ###

    ### Step 3: Get functional-to-standard image registration ###

	  # Get functional-to-anatomical image registration
	  flirt -omat func2anat.mat -cost corratio -dof 12 -interp trilinear -ref \
          /home/medialab/data/ADNI/process_test/MRI/MRI_$MRI_ID/skullstrip.nii \
          -in despike0050.nii

    # Get anatimical-to-standard image registration
	  flirt -omat anat2stnd.mat -cost corratio -dof 12 -interp trilinear -ref \
          ~/data/template/std_skullstrip.nii.gz -in \
          /home/medialab/data/ADNI/process_test/MRI/MRI_$MRI_ID/skullstrip.nii

    # apply MRI to standard registration
	  flirt -out registration_T1.nii -interp trilinear -applyxfm -init anat2stnd.mat \
          -ref ~/data/template/std_skullstrip.nii.gz -in \
          /home/medialab/data/ADNI/process_test/MRI/MRI_$MRI_ID/skullstrip.nii

    # Get functional-to-standard image transformation
	  convert_xfm -omat func2stnd.mat -concat anat2stnd.mat func2anat.mat

    despike_fileNo=`ls despike*.nii | wc`
	  despike_fileNo=($despike_fileNo)
	  despike_fileNo=${despike_fileNo[0]}
	  
	  echo $despike_fileNo
	  ## Apply functional-to-standard image registration
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
	      
	      flirt -out registration_fMRI_$fMRI_index.nii -interp trilinear -applyxfm \
              -init func2stnd.mat -ref ~/data/template/std_skullstrip.nii.gz -in despike$fMRI_index.nii
	      i=`expr $i + 1`
	  done

    fslmerge -t registration_fMRI_4d.nii registration_fMRI*.nii
	  ### Step 3: ends ###


	  ### Step 4: Remove noise signal ###

	  ## segment anatomical image
	  fsl5.0-fast -o T1_segm_A -t 1 -n 3 -g -p registration_T1.nii

	  ## Get mrean signal of CSF segment
	  3dmaskave -quiet -mask T1_segm_A_seg_0.nii registration_fMRI_4d.nii > fMRI_csf.1D

	  ## motion correction in the standard space
	  3dvolreg -prefix _mc_F.nii -1Dfile fMRI_motion.1D -Fourier -twopass \
             -zpad 4 -base 50 registration_fMRI_4d.nii

	  ## Get motion derivative
	  1d_tool.py -write fMRI_motion_deriv.1D -derivative -infile fMRI_motion.1D

	  ## concatenate CSF signal, motion correction, motion derivative into 'noise signal'
	  1dcat fMRI_csf.1D fMRI_motion.1D fMRI_motion_deriv.1D > fMRI_noise.1D

	  ## Regress out the 'noise signal' from functional image
	  3dBandpass -prefix fMRI_removenoise.nii -mask registration_fMRI_0003.nii \
               -ort fMRI_noise.1D 0.01 0.08 registration_fMRI_4d.nii



    # cannot make sure all nii files are valid, so need the time stamp now


    
}
