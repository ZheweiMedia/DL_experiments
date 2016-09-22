%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%   1. Step4. After After_SPM.m
%   2. Now the fMRI files are all matched with AAL template, we need to
%       separate fMRI files as 120 zones as AAL.
%   3. How to do it faster other than travel all the pixels? Separate AAL 
%       template as 120 matrix, and for each matrix its corresponding zone is 
%       1 and others are 0. Then do pointwise multiplication.
%
%
%
%
%
%

fMRI_IID = [346237];

Path_fMRI = './data/AD_data/fMRI_SPM_%d.txt';
addpath(genpath('Tools/NIfTI_Tools/'));
%% index of AAL2
[index, Label, value] = textread('/home/medialab/spm12/atlas/aal2.nii.txt','%u %s %u');
% then make a dictionary
[i_index,~] = size(index);
dictionary = zeros(i_index, 2);% map index and value
dictionary(:,1) = index;
dictionary(:,2) = value;

AAL_nii = load_nii('/home/medialab/spm12/atlas/AAL2.nii');
AAL_matrices = cell(1, 120); % 120 zones
for iMatrix = 1:120
    aal_matrix = AAL_nii.img;
    aal_matrix(aal_matrix ~= dictionary(iMatrix,2)) = 0;
    aal_matrix(aal_matrix == dictionary(iMatrix,2)) = 1;
    AAL_matrices{iMatrix} = aal_matrix;
end

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
        sum(sum(sum(fMRI_nii.img.*AAL_matrices{10})))
    end
end
    