#!/bin/bash


# cat the result of MatLab belongs to the same subject to a file 

# for different groups change the line of cat


cd /home/medialab/data/ADNI/ADNI
# list the samples we want to process
IIDarray=(  238623 240811 243902 223896 233437 \
254581 257271 259654 259806 260580 \
395980 268914 279472 281887 \
283913 238542 \
296769 296863 300088 308182 262078 \
268925 266634  273503 269279 \
315850 234917 255986 280365 \
282646 290815 289559 289656 387091 \
334140 322060 316542 350735 317121 \
266208 267713 365086 264214 279084 \
308403 308418   )

XMLS=`find ./ -name "*Resting_State_fMRI*.xml"`

for X in $XMLS
do
    iid=`xmllint --xpath '//project/subject/study/series/imagingProtocol/imageUID/text()' $X`
    subj=`xmllint --xpath '//project/subject/subjectIdentifier/text()' $X`
    case "${IIDarray[@]}" in  *$iid*)
        echo $iid
        cat /home/medialab/Zhewei/data/NC_Results/NC_Result${iid}.txt >> /home/medialab/Zhewei/data/NC_Results/NC_Subj${subj}_Baseline
    esac
done
