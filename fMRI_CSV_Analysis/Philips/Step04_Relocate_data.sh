#!/bin/bash

# after we generate the clean image IDs, we need to relocate them as groups.
# so basically we separate them as MRI folder and fMRI folder, and in each folder,
# the image folder is named as their image ID.

# How to use: bash Step04_relocate_data.sh Clean_fMRI_ImageID Clean_MRI_ImageID 


# first, load MRI and fMRI image IDs

fMRI_IDs=`cat ~/Zhewei/fMRI_CSV_Analysis/$1`
MRI_IDs=`cat ~/Zhewei/fMRI_CSV_Analysis/$2`


# second, go to ADNI folder to read xml files
cd /home/medialab/data/ADNI/ADNI
MRI_XMLS=`find ./ -name "*MPRAGE*.xml"`
fMRI_XMLS=`find ./ -name "*Resting_State_fMRI*.xml"`

mkdir /home/medialab/data/ADNI/MRI
mkdir /home/medialab/data/ADNI/fMRI

for X in $MRI_XMLS;
do
    iid=`xmllint --xpath '//project/subject/study/series/imagingProtocol/imageUID/text()' $X`
    case "${MRI_IDs[@]}" in
        *$iid*)
            # find all dcm file for this MRI image
            dcm_MRI=`find $PWD -name "*_MR_MPRAGE_*${iid}*.dcm"`
            # copy all dcm to MRI folder
            mkdir /home/medialab/data/ADNI/MRI/MRI_${iid}
            cp $dcm_MRI /home/medialab/data/ADNI/MRI/MRI_${iid}
    esac
done

for X in $fMRI_XMLS;
do
    iid=`xmllint --xpath '//project/subject/study/series/imagingProtocol/imageUID/text()' $X`
    case "${fMRI_IDs[@]}" in
        *$iid*)
            # find all dcm file for this fMRI image
            dcm_fMRI=`find $PWD -name "*Resting_State_fMRI*${iid}*.dcm"`
            # copy all dcm to fMRI folder
            mkdir /home/medialab/data/ADNI/fMRI/fMRI_${iid}
            cp $dcm_fMRI /home/medialab/data/ADNI/fMRI/fMRI_${iid}
    esac
done


