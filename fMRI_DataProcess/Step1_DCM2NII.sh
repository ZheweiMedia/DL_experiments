#!/bin/bash

Scan_all_folder () {
# go to the fold which contain the files

cd /home/medialab/data/ADNI/ADNI
# list the samples we want to process
IIDarray=( 213885 180734 199148 243875 316041 \
381524 191820 207955 256635 223330 \
192250 207666 257487 332881 393007 \
258448 279226 301767 346233 395573 \
278818 300245 323843 361436 414381 \
283879 305240 326318 358424 417987 \
311921 332859 354814 379008 307555 \
307553 334236 334235 350115 350113 \
381403 246032 265869 306576 372938 \
248233 265533 290438 336704 385092 \
255318 274437 301834 393850 319132 \
376489 361973 388039 343905 361116 \
372823 398098 261316 261319 225058 \
242252 305412 286425 241661 257106 \
339828 264416 281497 308391 347747 \
320432 337377 352722 367848 332584 \
347725 364273 390419 252603 199197 \
224635 280337 352437 402257 255135 \
202425 226625 243008 207341 222174 \
274112 351336 399918 247852 207991 \
223649 281032 353098 404042 290305 \
321928 362541 311906 338289 353986 \
378012 319541 346592 358601 386888 \
260905 277297 301221 341866 398232 \
300529 316049 343137 370437 183884 \
215435 181505 193431 242177 310476 \
379344 217608 184535 196434 247662 \
316979 382683 240043 208974 223353 \
275532 354598 226190 243115 259900 \
297463 367820 249144 264701 284291 \
329780 387206 281149 299318 324478 \
357940 339436 354860 367326 394943 \
401558 264531 228463 245122 305210 \
374515 283305 247533 267918 319578 \
382880 289331 307991 337186 306672 \
333641 376324 316519 337220 354697 \
383934 235258 298266 317378 344443 \
377061 300841 316406 347906 375664 \
361367 317397 336187 266223 232243 \
247983 302589 372302 272899 240902 \
257011 316276 385078 256753 297616 \
259332 281083 341127 394175 279103 \
297702 374201 358935 412933 278493 \
305261 374165 374144 407059 279181 \
301103 319553 358798 414279 282297 \
303032 323821 361486 323163 323157 \
349748 374318 392890 293995 335381 \
341976  )
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
