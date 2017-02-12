#!/bin/bash

# after we generate the clean image IDs, we need to relocate them as groups.
# so basically we separate them as MRI folder and fMRI folder, and in each folder,
# the image folder is named as their image ID.

# How to use: bash Step03_relocate_data.sh Clean_fMRI_ImageID Clean_MRI_ImageID 


# first, load MRI and fMRI image IDs

fMRI_IDs=`cat ~/Zhewei/fMRI_CSV_Analysis/SIEMENS/$1`
MRI_IDs=`cat ~/Zhewei/fMRI_CSV_Analysis/SIEMENS/$2`


# second, go to ADNI folder to read xml files
cd /home/medialab/data/ADNI/SIEMENS/ADNI/
MRI_XMLS=`find ./ -name "*MPRAGE*.xml"`
fMRI_XMLS=`find ./ -name "*MoCoSeries*.xml"`

mkdir /home/medialab/data/ADNI/SIEMENS/MRI
mkdir /home/medialab/data/ADNI/SIEMENS/fMRI

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
            # find all dcm file for this MRI image
            dcm_MRI=`find $PWD -name "*_MPRAGE_*${iid}*.dcm"`
            # copy all dcm to MRI folder
            mkdir /home/medialab/data/ADNI/SIEMENS/MRI/MRI_${iid}_${timeFilt}
            cp $dcm_MRI /home/medialab/data/ADNI/SIEMENS/MRI/MRI_${iid}_${timeFilt}
    esac
done

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
            # find all dcm file for this fMRI image
            dcm_fMRI=`find $PWD -name "*_MoCoSeries_*${iid}*.dcm"`
            # copy all dcm to fMRI folder
            mkdir /home/medialab/data/ADNI/SIEMENS/fMRI/fMRI_${iid}_${timeFilt}
            cp $dcm_fMRI /home/medialab/data/ADNI/SIEMENS/fMRI/fMRI_${iid}_${timeFilt}
    esac
done


