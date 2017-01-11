#~/bin/bash

# After SPM processing, copy a time step to preprocess_check fold.
# ImageID now in AD_Filter or NC_Filter
# bash Check_Preprocess.sh AD_Filter or
# bash Check_Preprocess.sh NC_Filter

cd /home/medialab/data/ADNI

IIDarray=`cat ~/Zhewei/fMRI_SubjectAnalysis/$1`
echo $IIDarray

# read all samples
XMLS=`find ./ -name "*Resting_State_fMRI*.xml"`

for X in $XMLS
do
    iid=`xmllint --xpath '//project/subject/study/series/imagingProtocol/imageUID/text()' $X`
    time=`xmllint --xpath '//project/subject/study/series/dateAcquired/text()' $X`
    # echo $iid
    # find out the correct time for .nii time. Because after dcm2nii, sometimes we have more
    # than 140 nii files for one subject.
    timeYear=${time:0:4}
    timeMonthDay=${time:5:5}
    timeMonth=${timeMonthDay:0:2}
    timeDay=${timeMonthDay:3:4}
    timeFilt=$timeYear$timeMonth$timeDay

    case "${IIDarray[@]}" in  *$iid*)
				  cp /home/medialab/data/ADNI/fMRI_${iid}/*$timeFilt*_*_100.nii /home/medialab/data/ADNI/fMRI_check/fMRI_${iid}.nii
    esac
done
				  
