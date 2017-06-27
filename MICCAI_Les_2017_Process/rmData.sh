cd /home/medialab/Zhewei/MICCAI_Les_2017_Process/data/train




index_i=(1 2 3 4 5 6 7 8 9)
index_j=(0 1 2 3 4 5 6 7 8 9)

for i in "${index_i[@]}"
do
    for j in "${index_j[@]}"
    do
        echo $i$j
        rm sample$i$j*
        rm label$i$j*
    done
done

