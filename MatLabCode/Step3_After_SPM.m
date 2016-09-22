%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%
%   1. The program used to pocess the fMRI files after SPM.
%       In SPM, if we use B-spline Interpolation, there will be negative
%       intensity values appear. Because the negative values very few 
%       and almost distributed over skull (out of AAL), so we can simply re-set
%       the values as 0.
%   
%   2. How to use it? 
%       Before run this program, run the shell script and generate the
%       links to fMRI files which processed by SPM.
%       Every time set the fMRI_IID, and the path for the txt
%       which contain the links to the fMRI.
%
%   Zhewei @ 9/21/2016
%



fMRI_IID = [372599, 400431, 345555, 358811, 372471, ...
            415205, 228872, 248870, 263860, 297847, ...
            357475, 372254, 389296, 415178, 376933, ...
            368413, 291229, 323796, 347092, 295969, ...
            316009, 342048, 367094, 300043, 322371, ...
            342223, 369943, 306375, 335235, 352396];

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

