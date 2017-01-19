#!/bin/bash

# use for rename fMRI folders
# usage: bash Step05_Add_time_stamp.sh Clean_fMRI_ImageID Clean_MRI_ImageID 


# first, load fMRI image IDs
fMRI_IDs=`cat ~/Zhewei/fMRI_CSV_Analysis/Philips/$1`
MRI_IDs=`cat ~/Zhewei/fMRI_CSV_Analysis/Philips/$2`

# second, go to ADNI folder to read xml files
cd /home/medialab/data/ADNI/Philips/ADNI
fMRI_XMLS=`find ./ -name "*Resting_State_fMRI*.xml"`
MRI_XMLS=`find ./ -name "*MPRAGE*.xml"`

for X in $fMRI_XMLS;
do
    iid=`xmllint --xpath '//project/subject/study/series/imagingProtocol/imageUID/text()' $X`
    # IMPORTANT:
    time=`xmllint --xpath '//project/subject/study/series/dateAcquired/text()' $X`

    # string of time in files
    timeYear=${time:0:4}
    timeMonthDay=${time:5:5}
    timeMonth=${timeMonthDay:0:2}
    timeDay=${timeMonthDay:3:4}
    timeFilt=$timeYear$timeMonth$timeDay

    case "${fMRI_IDs[@]}" in
        *$iid*)
            mv /home/medialab/data/ADNI/Philips/fMRI/fMRI_${iid} /home/medialab/data/ADNI/Philips/fMRI/fMRI_${iid}_${timeFilt}
    esac
done


for X in $MRI_XMLS;
do
    iid=`xmllint --xpath '//project/subject/study/series/imagingProtocol/imageUID/text()' $X`
    # IMPORTANT:
    time=`xmllint --xpath '//project/subject/study/series/dateAcquired/text()' $X`

    # string of time in files
    timeYear=${time:0:4}
    timeMonthDay=${time:5:5}
    timeMonth=${timeMonthDay:0:2}
    timeDay=${timeMonthDay:3:4}
    timeFilt=$timeYear$timeMonth$timeDay

    case "${MRI_IDs[@]}" in
        *$iid*)
            mv /home/medialab/data/ADNI/Philips/MRI/MRI_${iid} /home/medialab/data/ADNI/Philips/MRI/MRI_${iid}_${timeFilt}
    esac
done

