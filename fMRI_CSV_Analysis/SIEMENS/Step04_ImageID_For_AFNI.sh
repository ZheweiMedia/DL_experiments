#!/bin/bash

# Now we have fMRI_IDs, and MRI_IDs, we need to get the IDs with time stamp.

# bash Step06_ImageID_For_AFNI.sh Clean_fMRI_ImageID Clean_MRI_ImageID SIEMENS


fMRI_IDs=(`cat ~/Zhewei/fMRI_CSV_Analysis/SIEMENS/$1`)
MRI_IDs=(`cat ~/Zhewei/fMRI_CSV_Analysis/SIEMENS/$2`)
Folder_name=$3


for id in ${fMRI_IDs[@]};
do
    cd ~/data/ADNI/$Folder_name/fMRI/
    echo `ls -d -- fMRI_$id*` >> ~/Zhewei/fMRI_CSV_Analysis/SIEMENS/fMRI_IDs
    echo $id >> ~/Zhewei/fMRI_CSV_Analysis/SIEMENS/pair_with_fMRI_IDs
done

for id in ${MRI_IDs[@]};
do
    cd ~/data/ADNI/$Folder_name/MRI/
    echo `ls -d -- MRI_$id*` >> ~/Zhewei/fMRI_CSV_Analysis/SIEMENS/MRI_IDs
    echo $id >> ~/Zhewei/fMRI_CSV_Analysis/SIEMENS/pair_with_MRI_IDs
done

