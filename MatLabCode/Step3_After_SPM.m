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



fMRI_IID = [326298, 361294, 337404, 363620, 283913,... 
            319211, 350450, 238540, 238542, 253525, ...
            296769, 352724, 375151, 296863, 369618, ...
            340743, 368950, 300088, 314505, 343935, ...
            368923, 308182, 262078, 296612, 320519, ...
            268925, 297183, 321439, 401398, 266634];

Path_fMRI = './data/Normal_data/fMRI_SPM_%d.txt';
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

