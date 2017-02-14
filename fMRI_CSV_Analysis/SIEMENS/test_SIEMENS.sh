rm -r /home/medialab/data/ADNI/process_test_SIEMENS

mkdir /home/medialab/data/ADNI/process_test_SIEMENS

mkdir /home/medialab/data/ADNI/process_test_SIEMENS/fMRI
mkdir /home/medialab/data/ADNI/process_test_SIEMENS/MRI

bash Step03_Relocate_data.sh test_Clean_fMRI_ImageID test_Clean_MRI_ImageID

mv ~/data/ADNI/SIEMENS/fMRI/* ~/data/ADNI/process_test_SIEMENS/fMRI/
mv ~/data/ADNI/SIEMENS/MRI/* ~/data/ADNI/process_test_SIEMENS/MRI/


