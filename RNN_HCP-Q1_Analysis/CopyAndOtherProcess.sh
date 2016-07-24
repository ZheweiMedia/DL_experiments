#!/bin/bash

# 1. copy the data from HCP-Q1 disk to PC disk.
# 2. gzip -d, and dcm2nii
# 3. get the list of 3D nii
# 4. SPM12 process, matlab process.
# 5. copy all results file to ./Zhewei/data/HCP_data


IIDarray=(100307 103515 103818 111312 114924 \
117122 118932 119833 120212 125525 128632 130013 \
131621 137128 138231 142828 143325 144226 149337 \
150423 153429 156637 159239 161731 162329 167743 \
172332 182739 191437 192439 192540 194140 197550 \
199150 199251 200614 201111 210617 217429 249947 \
250427 255639 304020 307127 329440 355542 499566 \
530635 559053 585862 611231 638049 665254 672756 \
685058 729557 732243 792564 826353 856766 859671 \
861456 865363 877168 889579 894673 896778 896879 \
901139 917255 937160  )

# Classarray=('EMOTION' 'GAMBLING' 'LANGUAGE' 'MOTOR' \
              # 'RELATIONAL' 'SOCIAL' 'WM')
              
Classarray=('EMOTION' 'RELATIONAL')

for ID in ${IIDarray[@]}
do
    echo $ID
    mkdir /home/medialab/data/HCP-Q1/tfMRI/$ID
    for class in ${Classarray[@]}
    do
        echo $class
        mkdir /home/medialab/data/HCP-Q1/tfMRI/$ID/$class
        fileName=/media/medialab/HCP-Q1/$ID/unprocessed/3T/tfMRI_$class\_LR/$ID\_3T_tfMRI_$class\_LR.nii.gz
        # cp $fileName /home/medialab/data/HCP-Q1/tfMRI/$ID/$class
        cd /home/medialab/data/HCP-Q1/tfMRI/$ID/$class
        fileAddress=/home/medialab/data/HCP-Q1/tfMRI/$ID/$class
        # gzip -d *.nii.gz
        # dcm2nii *.nii < /home/medialab/tmp/tmp.txt
        cp $ID\_$class\_results.txt /home/medialab/Zhewei/data/HCP_data/
        for niifile in $(ls f*.nii)
        do
            echo $fileAddress'/'$niifile
            echo $fileAddress'/'$niifile >> $ID\_$class.txt
            # rm $ID\_$class.txt
        done
        
    done
done
