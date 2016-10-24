#!/bin/bash

cd /home/medialab/data/Weizmann_Seg/1obj/

folds=($(ls -1))

echo $folds

declare -i No=0

for i_file in "${folds[@]}"
do
    echo $i_file
    echo $No
    cd /home/medialab/data/Weizmann_Seg/1obj/$i_file/human_seg/
    files=($(ls -1))
    # cp ${files[0]} /home/medialab/data/Weizmann_Seg/Labels/$No.png
    cd /home/medialab/data/Weizmann_Seg/1obj/$i_file/src_bw/
    files=($(ls -1))
    cp ${files[0]} /home/medialab/data/Weizmann_Seg/Img_BW/$No.png
    cd /home/medialab/data/Weizmann_Seg/1obj/
    No=$((No+1))
done
echo $No
