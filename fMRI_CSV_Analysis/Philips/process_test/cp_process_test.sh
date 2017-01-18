#!/bin/bash

cd /home/medialab/data/ADNI/Philips/MRI/

cp -r MRI_238627 MRI_303066 MRI_240812 MRI_304793 MRI_371991 ../process_test/MRI/

cd /home/medialab/data/ADNI/Philips/fMRI/

cp -r fMRI_238623 fMRI_303069 fMRI_240811 fMRI_304790 fMRI_371994 ../process_test/fMRI/
