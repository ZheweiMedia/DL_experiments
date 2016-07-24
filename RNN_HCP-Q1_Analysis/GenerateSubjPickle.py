"""
7/24/2016 start:

This program used to generate general pickle files from the raw data from MatLab.

This time we change the strategy: store the data in a data structure: a dict, and then

save the whole data as a pickle file.

Classes and frames and Label: 

'EMOTION'       176         0
'GAMBLING'      253
'LANGUAGE'      316
'MOTOR'         284
'RELATIONAL'    232         1
'SOCIAL'        274
'WM'            405


all data read or write in ./data/HCP_data/



******************************************
1. Set group label.
2. Set how many sans with noise will generate.
3. Set postfix name for output pickle. '.pickle.gz' for no-noise, '_noise.pickle.gz' for noise data.
4. Make sure input correct .txt files.
5. Add some code to check if value is Nan. It happened for a subject of LMCI. Don't know why. 
   So now if the file contains Nan, will print the file name.(maybe we can do better.)
******************************************

Usage:  python3.5 data/AD_Results/AD_Subj*.txt

Output: an array with the 3D shape SampleNo*FrameNo*FeatureNo and label for each sample

@Zhewei


"""
