#!/bin/bash

Scan_all_folder () {
# go to the fold which contain the files

cd /home/medialab/data/ADNI/ADNI
# list the samples we want to process
IIDarray=( 251176 322050 385942 274147 352947 \
404373 227595 292427 249536 267490 \
287274 256148 273181 293284 338109 \
257477 274134 296652 335317 394820 \
258528 273556 298203 285812 306320 \
330179 363568 296366 313307 341806 \
367496 306889 333755 352349 375097 \
266129 266131 283851 283853 306280 \
306277 348071 348075 269256 269253 \
286375 286378 311356 311357 351592 \
404475 283267 283264 283272 283260 \
303143 303137 334609 334605 363293 \
303733 303731 323338 323324 348393 \
348396 376286 339123 339129 354587 \
371407 397506 247209 243880 260303 \
280649 318774 381846 220070 287005 \
363411 261166 278367 304270 324394 \
363421 300057 325672 342309 367838 \
339635 367161 323221 346564 361591 \
385234 261984 277286 302671 343304 \
415196 286477 305233 326518 362146 \
229511 249328 265957 305277 368901 \
235238 252282 270573 303434 360939 \
255284 269694 286940 338318 388696 \
255309 270542 291146 348195 391665 \
290644 310766 417557 364453 304675 \
328499 348153 373709 373711 354654 \
400360 341823 343366 259691 259693 \
280800 297561 342030 395958 267894 \
287082 304596 348045 398599 287650 \
308121 331236 362399 293629 313410 \
341317 364929 314327 340210 355856 \
495757 337131 352312 368186 394511 \
332647 330141 398432 281024 330138 \
330233 342476 375500  )
# read all samples
XMLS=`find ./ -name "*Resting_State_fMRI*.xml"`

declare -i fileShould=140

# compare them
for X in $XMLS
do
    iid=`xmllint --xpath '//project/subject/study/series/imagingProtocol/imageUID/text()' $X`
    time=`xmllint --xpath '//project/subject/study/series/dateAcquired/text()' $X`
    # echo $iid
    timeYear=${time:0:4}
    timeMonthDay=${time:5:5}
    timeMonth=${timeMonthDay:0:2}
    timeDay=${timeMonthDay:3:4}
    timeFilt=$timeYear$timeMonth$timeDay
    
    # echo $timeFilt
    No=$fileShould
    case "${IIDarray[@]}" in  *$iid*)
        # find sid to identify .dcm files
        # sid=`xmllint --xpath '//project/subject/subjectIdentifier/text()' $X`
        # find the path to .dcm
        dcm_fMRI=`find $PWD -name "*Resting_State_fMRI*${iid}*.dcm"`
        # cp .dcm to new fold, then dcm2nii, then delete .dcm in the new fold
        mkdir /home/medialab/data/ADNI/fMRI_${iid}
        cp $dcm_fMRI /home/medialab/data/ADNI/fMRI_${iid}
        dcm2nii  -g n -n y /home/medialab/data/ADNI/fMRI_${iid}
        del_dcmFile=`find /home/medialab/data/ADNI/fMRI_${iid}/ -name "*.dcm"`
        # rm $del_dcmFile
        # find all .nii file, and output the full path to a .txt file
        # here should use some filt to remove the .nii files that not belongs to
        # the 140 niis.
        nii_file=`find /home/medialab/data/ADNI/fMRI_${iid}/  -name "*$timeFilt*_*_*.nii"`
        No=0
        for nii in $nii_file
        do
            readlink -f $nii >> fMRI_${iid}.txt
            No=`expr $No + 1`
        done
    esac
    if [ $No -ne $fileShould ]
    then
        echo $iid
        echo $iid >> fMRI_Fail.txt
    fi
    # echo $No # check how many files
done
}
Scan_all_folder
