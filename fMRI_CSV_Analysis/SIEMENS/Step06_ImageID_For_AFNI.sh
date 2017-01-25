#!/bin/bash

# Now we have fMRI_IDs, and MRI_IDs, we need to get the IDs with time stamp.


fMRI_IDs=(`cat ~/Zhewei/fMRI_CSV_Analysis/Philips/$1`)
MRI_IDs=(`cat ~/Zhewei/fMRI_CSV_Analysis/Philips/$2`)

rm ~/data/ADNI/Philips/fMRI/fMRI_IDs
rm ~/data/ADNI/Philips/MRI/MRI_IDs

for id in ${fMRI_IDs[@]};
do
    cd ~/data/ADNI/Philips/fMRI/
    echo `ls -d -- fMRI_$id*` >> fMRI_IDs
done

for id in ${MRI_IDs[@]};
do
    cd ~/data/ADNI/Philips/MRI/
    echo `ls -d -- MRI_$id*` >> MRI_IDs
done

