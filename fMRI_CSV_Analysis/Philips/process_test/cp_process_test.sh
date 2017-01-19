#!/bin/bash
cd /home/medialab/data/ADNI/process_test/
rm -r *

mkdir ./MRI
mkdir ./fMRI


cd /home/medialab/data/ADNI/Philips/MRI/

cp -r MRI_238627 MRI_303066 MRI_240812 MRI_304793 MRI_371991 ../../process_test/MRI/

cd /home/medialab/data/ADNI/Philips/fMRI/

cp -r fMRI_238623_20110602 fMRI_303069_20120510 fMRI_240811_20110616 fMRI_304790_20120515 fMRI_371994_20130510 ../../process_test/fMRI/
