%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%   1. Do preprocssing via Afni, then we have 136 nii files.
%   2. Use matlab to calculate the avarage of the zones.
%
%
%
%

%% 

clear all

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
AAL_mask = AAL_nii.img;
AAL_b_mask = AAL_mask>0.001;
for iMatrix = 1:zones_No
    aal_matrix = AAL_nii.img;
    aal_matrix(aal_matrix ~= dictionary(iMatrix,2)) = 0;
    aal_matrix(aal_matrix == dictionary(iMatrix,2)) = 1;
    % How many pixels for each zone?
    AAL_PixelNO(iMatrix) = sum(sum(sum(aal_matrix)));
    AAL_matrices{iMatrix} = double(aal_matrix);
end


%% fMRI part
fMRI_data = cell(1, 1);

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
        % tmp_img = tmp_img.*AAL_b_mask;
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




