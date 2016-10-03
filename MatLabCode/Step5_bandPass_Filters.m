%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%
%   For bandpass filters
%   1. Read .mat files in.
%   2. Bandpass and save.
%
%
%


clear all

fMRI_IID = [346237, 358614, 372812, 398684, 264986, ...
            264987, 293808, 293809, 335306, 335307, ...
            390346, 258600, 258605, 272407, 272411, ...
            302039, 302042, 340021, 340024, 393209, ...
            287992, 287986, 310931, 310925, 336552, ...
            336551, 322009, 322000];
        
%% read files in

cd ~/Zhewei/data/data_from_SPM/

[~,numfiles] = size(fMRI_IID);

for ifile = 1:numfiles
    fileID = fMRI_IID(ifile);
    mat_name = strcat(num2str(fMRI_IID(ifile)), '.mat');
    feature = load(mat_name);
end