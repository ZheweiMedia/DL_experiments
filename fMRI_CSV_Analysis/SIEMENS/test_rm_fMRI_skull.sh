#!/bin/bash

# use for preprocessing data
# usage: bash Step10_preprocessing.sh fMRI_IDs MRI_IDs Philips 3

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

    cd /home/medialab/data/ADNI/$folder_name/fMRI/$fMRI_postFix/niiFolder
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
    # !!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!! T1.nii
    # dof set as 6, so now it is rigid registration
	  flirt -omat func2anat.mat -cost corratio -dof 6 -interp trilinear -ref \
          /home/medialab/data/ADNI/$folder_name/MRI/$MRI_postFix/skullstrip.nii \
          -in despike0050.nii

    # Get anatimical-to-standard image registration
	  flirt -omat anat2stnd.mat -cost corratio -dof 12 -interp trilinear -ref \
          ~/data/template/std_skullstrip.nii.gz -in \
          /home/medialab/data/ADNI/$folder_name/MRI/$MRI_postFix/skullstrip.nii

    # apply MRI to standard registration
	  flirt -out registration_T1.nii -interp trilinear -applyxfm -init anat2stnd.mat \
          -ref ~/data/template/std_skullstrip.nii.gz -in \
          /home/medialab/data/ADNI/$folder_name/MRI/$MRI_postFix/skullstrip.nii

    # Get functional-to-standard image transformation
	  convert_xfm -omat func2stnd.mat -concat anat2stnd.mat func2anat.mat

    despike_fileNo=`ls despike*.nii | wc`
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
              -init func2anat.mat -ref ~/data/ADNI/$folder_name/MRI/$MRI_postFix/skullstrip.nii \
              -in despike$fMRI_index.nii

        # remove the skull of fMRI
        3dcalc -prefix fMRI_skullstrip_$fMRI_index.nii -expr 'a*step(b)' \
               -b ~/data/ADNI/$folder_name/MRI/$MRI_postFix/skullstrip_mask.nii \
               -a fMRI_in_MRI_space_$fMRI_index.nii
	      
	      flirt -out registration_fMRI_$fMRI_index.nii -interp trilinear -applyxfm \
              -init anat2stnd.mat -ref ~/data/template/std_skullstrip.nii.gz -in fMRI_skullstrip_$fMRI_index.nii
	      i=`expr $i + 1`
	  done

    fslmerge -t registration_fMRI_4d.nii registration_fMRI*.nii
	  ### Step 3: ends ###


    ### Step 4: Remove noise signal ###

	  ## segment anatomical image
	  fsl5.0-fast -o T1_segm_A -t 1 -n 3 -g -p /home/medialab/data/ADNI/$folder_name/MRI/$MRI_postFix/skullstrip.nii

    
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
