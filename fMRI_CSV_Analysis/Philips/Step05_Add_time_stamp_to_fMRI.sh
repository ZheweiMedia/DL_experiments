#!/bin/bash

# use for rename fMRI folders


# first, load fMRI image IDs
fMRI_IDs=`cat ~/Zhewei/fMRI_CSV_Analysis/Philips/$1`

# second, go to ADNI folder to read xml files
cd /home/medialab/data/ADNI/Philips/ADNI
fMRI_XMLS=`find ./ -name "*Resting_State_fMRI*.xml"`

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

