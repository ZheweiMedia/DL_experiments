#!/bin/bash


# cat the result of MatLab belongs to the same subject to a file 

# for different groups change the line of cat


cd /home/medialab/data/ADNI/ADNI
# list the samples we want to process
IIDarray=(  251176 274147 227595 249536 256148 \
257477 258528 285812 296366 306889 \
266129 269256 283267 303733 339123 \
247209 243880 220070 261166 278367 \
300057 339635 323221 261984 286477 \
229511 235238 255284 255309 290644 \
304675 354654 341823 343366 259691 \
267894 287650 293629 314327 337131 \
332647 330141 281024 330233 342476 \
375500  )

XMLS=`find ./ -name "*Resting_State_fMRI*.xml"`

for X in $XMLS
do
    iid=`xmllint --xpath '//project/subject/study/series/imagingProtocol/imageUID/text()' $X`
    subj=`xmllint --xpath '//project/subject/subjectIdentifier/text()' $X`
    case "${IIDarray[@]}" in  *$iid*)
        echo $iid
        cat /home/medialab/Zhewei/data/LMCI_Results/LM_Result${iid}.txt >> /home/medialab/Zhewei/data/LMCI_Results/LM_Subj${subj}_Baseline
    esac
done
