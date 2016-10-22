#!/bin/bash

cd /home/medialab/data/Weizmann_Seg/1obj/

folds=($(ls -1))

echo $folds

declare -i No=0

for i in "${folds[@]}"
do
    echo $i
    cd /home/medialab/data/Weizmann_Seg/1obj/$i/human_seg/
    files=($(ls -1))
    cp ${files[0]} /home/medialab/data/Weizmann_Seg/Labels/$No.png
    cd /home/medialab/data/Weizmann_Seg/1obj/$i/src_color/
    files=($(ls -1))
    cp ${files[0]} /home/medialab/data/Weizmann_Seg/Img/$No.png
    cd /home/medialab/data/Weizmann_Seg/1obj/
    No=$((No+1))
done
echo $No
