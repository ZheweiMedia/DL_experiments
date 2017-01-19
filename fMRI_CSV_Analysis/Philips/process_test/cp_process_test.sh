#!/bin/bash
cd /home/medialab/data/ADNI/process_test/
rm -r *

mkdir ./MRI
mkdir ./fMRI


cd /home/medialab/data/ADNI/Philips/MRI/

cp -r MRI_238627_20110602 MRI_303066_20120510 MRI_240812_20110616 MRI_304793_20120515 MRI_371991_20130510 ../../process_test/MRI/

cd /home/medialab/data/ADNI/Philips/fMRI/

<<<<<<< HEAD
cp -r fMRI_238623_20110602 fMRI_240811_20110616 fMRI_303069_20120510 fMRI_304790_20120515 fMRI_371994_20130510 ../../process_test/fMRI/
=======
cp -r fMRI_238623_20110602 fMRI_303069_20120510 fMRI_240811_20110616 fMRI_304790_20120515 fMRI_371994_20130510 ../../process_test/fMRI/
>>>>>>> dd57e99c1201f5d54642996af915db2afa2cb4cb
