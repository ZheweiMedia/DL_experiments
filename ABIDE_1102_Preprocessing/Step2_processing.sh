#! bin/bash

# This program use for moving data
#
#
#



initial_dataFolder=$1
process_dataFolder=$2

cd $initial_dataFolder

# read all .xml file, separate as ABIDE or Control

xmlfiles=`ls *Resting_State_fMRI*.xml`

for xmlfile in $xmlfiles; do
    echo ''
    echo xmlfile: $xmlfile

    subjectID=`xmllint --xpath '//project/subject/subjectIdentifier/text()' $xmlfile`
    group=`xmllint --xpath '//project/subject/researchGroup/text()' $xmlfile`
    echo $subjectID

    fMRI_fileNo=`ls ./$subjectID/Resting_State_fMRI/*/ | wc`
    arr=($fMRI_fileNo)

    if [ ${arr[0]} == 1 ]; then
        cd $process_dataFolder/$group/$subjectID/
	cd T1
	3dSkullStrip -o_ply skullstrip_musk.nii -input *.nii
	3dcalc -prefix skullstrip.nii -expr 'a*step(b)' -b skullstrip_musk.nii 
	cd ../fMRI
	# discard first 10 images 
	mv *.nii fMRI.nii
	fslsplit fMRI.nii fMRI
	i=1
	while [ $i -le 10 ];
	do
	    rm *00$i.nii
	    i=`expr $i + 1`
	done
	rm fMRI.nii
	fslmerge -t fMRI_4d.nii *.nii
	rm fMRI0*.nii
	
	## slice timing
	3dTshift -prefix slicetiming.nii -tpattern altplus fMRI_4d.nii

	## motion correction
	3dvolreg -prefix motioncorrection.nii -1Dfile _motion.1D -Fourier -twopass -zpad 4 -base 50 slicetiming.nii

	## despike 
	3dDespike -prefix despike.nii -ssave _spikiness.nii motioncorrection.nii

	## splite and clean .nii files
	fslsplit despike.nii despike
	rm slicetiming.nii motioncorrection.nii despike.nii

	### Step 2: ends ###

	### Step 3: Get functional-to-standard image registration ###

	# Get functional-to-anatomical image registration
	flirt -omat func2anat.mat -cost corratio -dof 12 -interp trilinear -ref ../T1/skullstrip.nii -in despike0050.nii
	
	# Get anatimical-to-standard image registration
	flirt -omat anat2stnd.mat -cost corratio -dof 12 -interp trilinear -ref ~/data/template/std_skullstrip.nii.gz -in ../T1/skullstrip.nii

	# Get functional-to-standard image transformation
	convert_xfm -omat func2stnd.mat -concat anat2stnd.mat func2anat.mat

	## Apply 
	cd $initial_dataFolder
    fi
done
