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

clear all

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
            372599, 400431, 345555, 358811, 372471, ...
            415205, 228872, 248870, 263860, 297847, ...
            357475, 372254, 389296, 415178, 376933, ...
            368413, 291229, 323796, 347092, 295969, ...
            316009, 342048, 367094, 300043, 322371, ...
            342223, 369943, 306375, 335235, 352396];

Path_fMRI = './data/AD_data/fMRI_SPM_%d.txt';
addpath(genpath('Tools/NIfTI_Tools/'));
%% index of AAL2
frame_No = 130;
zones_No = 120;
[index, Label, value] = textread('/home/medialab/spm12/atlas/aal2.nii.txt','%u %s %u');
% then make a dictionary
[i_index,~] = size(index);
dictionary = zeros(i_index, 2);% map index and value
dictionary(:,1) = index;
dictionary(:,2) = value;

AAL_nii = load_nii('/home/medialab/spm12/atlas/AAL2.nii');
AAL_matrices = cell(1, zones_No); % 120 zones
AAL_PixelNO = zeros(1, zones_No); % How many pixels for each zone?
for iMatrix = 1:zones_No
    aal_matrix = AAL_nii.img;
    aal_matrix(aal_matrix ~= dictionary(iMatrix,2)) = 0;
    aal_matrix(aal_matrix == dictionary(iMatrix,2)) = 1;
    % How many pixels for each zone?
    AAL_PixelNO(iMatrix) = sum(sum(sum(aal_matrix)));
    AAL_matrices{iMatrix} = double(aal_matrix);
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
    feature = zeros(zones_No, frame_No);
    % normalize to gaussion (0,1)
    total_img = [];
    for jframe = 1:frame_No
        fMRI_nii = load_nii(fMRI_data{ifile}{jframe});
        tmp_img = double(fMRI_nii.img);
        total_img = [total_img;tmp_img];
    end
    [m_t, n_t, p_t] = size(total_img);
    total_img = reshape(total_img,m_t*n_t*p_t, 1);
    %total_img = normpdf(total_img);
    mean_total = mean(total_img);
    std_total = std(total_img);
        
    for jframe = 1:frame_No
        fMRI_nii = load_nii(fMRI_data{ifile}{jframe});
        img = double(fMRI_nii.img);
        [m_i, n_i, p_i] = size(img);
        img = reshape(img, m_i*n_i*p_i,1);
        img = (img-mean_total)/std_total;
        img = reshape(img, m_i, n_i, p_i);
        for kzone = 1:zones_No
            feature(kzone, jframe) = sum(sum(sum(img.*AAL_matrices{kzone})))/AAL_PixelNO(kzone);
        end
    end
    
    % save in .mat files
    mat_name = strcat('/home/medialab/Zhewei/data/data_from_SPM/',num2str(fMRI_IID(ifile)), '.mat');
    save(mat_name, 'feature');
end




%% %%%%%%%%%%%%%%% NC
clear all


fMRI_IID = [238623, 303069, 240811, 304790, 371994, ...
            243902, 322442, 286519, 361612, 287493, ...
            361431, 254581, 273218, 290923, 335999, ...
            391150, 257271, 274579, 297353, 340048, ...
            395105, 259654, 274825, 299159, 346113, ...
            397604, 259806, 260580];

Path_fMRI = './data/Normal_data/fMRI_SPM_%d.txt';
addpath(genpath('Tools/NIfTI_Tools/'));
%% index of AAL2
frame_No = 130;
zones_No = 120;
[index, Label, value] = textread('/home/medialab/spm12/atlas/aal2.nii.txt','%u %s %u');
% then make a dictionary
[i_index,~] = size(index);
dictionary = zeros(i_index, 2);% map index and value
dictionary(:,1) = index;
dictionary(:,2) = value;

AAL_nii = load_nii('/home/medialab/spm12/atlas/AAL2.nii');
AAL_matrices = cell(1, zones_No); % 120 zones
AAL_PixelNO = zeros(1, zones_No); % How many pixels for each zone?
for iMatrix = 1:zones_No
    aal_matrix = AAL_nii.img;
    aal_matrix(aal_matrix ~= dictionary(iMatrix,2)) = 0;
    aal_matrix(aal_matrix == dictionary(iMatrix,2)) = 1;
    % How many pixels for each zone?
    AAL_PixelNO(iMatrix) = sum(sum(sum(aal_matrix)));
    AAL_matrices{iMatrix} = double(aal_matrix);
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
    feature = zeros(zones_No, frame_No);
    % normalize to gaussion (0,1)
    total_img = [];
    for jframe = 1:frame_No
        fMRI_nii = load_nii(fMRI_data{ifile}{jframe});
        tmp_img = double(fMRI_nii.img);
        total_img = [total_img;tmp_img];
    end
    [m_t, n_t, p_t] = size(total_img);
    total_img = reshape(total_img,m_t*n_t*p_t, 1);
    %total_img = normpdf(total_img);
    mean_total = mean(total_img);
    std_total = std(total_img);
        
    for jframe = 1:frame_No
        fMRI_nii = load_nii(fMRI_data{ifile}{jframe});
        img = double(fMRI_nii.img);
        [m_i, n_i, p_i] = size(img);
        img = reshape(img, m_i*n_i*p_i,1);
        img = (img-mean_total)/std_total;
        img = reshape(img, m_i, n_i, p_i);
        for kzone = 1:zones_No
            feature(kzone, jframe) = sum(sum(sum(img.*AAL_matrices{kzone})))/AAL_PixelNO(kzone);
        end
    end
    
    % save in .mat files
    mat_name = strcat('/home/medialab/Zhewei/data/data_from_SPM/',num2str(fMRI_IID(ifile)), '.mat');
    save(mat_name, 'feature');
end

    