%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%
%   1. The program used to pocess the fMRI files after SPM.
%       In SPM, if we use B-spline Interpolation, there will be negative
%       intensity values appear. Because the negative values very few 
%       and almost distributed over skull (out of AAL), so we can simply re-set
%       the values as 0.
%   
%   2. How to use it? Every time set the fMRI_IID, and the path for the txt
%       which contain the links to the fMRI.
%
%   Zhewei @ 9/21/2016
%



fMRI_IID = [346237, 358614, 372812, 398684, 264986, ...
            264987, 293808, 293809, 335306, 335307, ...
            390346, 258600, 258605, 272407, 272411, ...
            302039, 302042, 340021, 340024, 393209, ...
            287992, 287986, 310931, 310925, 336552, ...
            336551, 322009, 322000, 346367, 346359, ...
            362021, 394330, 360323, 373417, 390453, ...
            301395, 321520, 343571, 306073, 327941, ...
            348646, 360317, 382187, 258955, 272535, ...
            300352, 341972, 396530, 396527, 280778, ...
            297106, 322347, 359770, 412884, 300334, ...
            317435, 343285, 363190, 343912, 358050, ...
            ];

Path_fMRI = './data/AD_data/fMRI_SPM_%d.txt';
addpath(genpath('Tools/NIfTI_Tools/'))
files_No = 130;

[~,numfiles] = size(fMRI_IID);
fMRI_data = cell(1, numfiles);

for ifile = 1:numfiles
    fileID = fMRI_IID(ifile);
    IIDfilename = sprintf(Path_fMRI, fileID);
    fMRI_data{ifile} = sort(importdata(IIDfilename));
end

for ifile = 1:numfiles
    display(ifile);
    for jfile = 1:files_No
        fMRI_nii = load_nii(fMRI_data{ifile}{jfile});
        fileName = strcat(fMRI_nii.fileprefix,'.nii');
        fMRI_nii.img(fMRI_nii.img<0) = 0;
        save_nii(fMRI_nii, fileName);
    end
end

