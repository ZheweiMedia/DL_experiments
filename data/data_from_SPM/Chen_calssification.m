%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%
%   1. Repeat Chen's method to classification.
%   2. Person independent.
%
%
%
%
%
%
%




cd ~/Zhewei/data/data_from_SPM/

load('dataList.mat')

% subjects: 48
subjectNo = 48;
index = randperm(subjectNo);
train_index = index(1:45);
test_index = index(46:end);

fMRI_train_NC_IID = [];
fMRI_train_AD_IID = [];
fMRI_test_IID = [];
Label_test = [];
for i_train = 1:45
    if strcmp(char(data{train_index(i_train),1}), 'AD')
        fMRI_train_AD_IID = [fMRI_train_AD_IID data{train_index(i_train),2}];
    else
        fMRI_train_NC_IID = [fMRI_train_NC_IID data{train_index(i_train),2}];
    end
end

for i_test = 1:3
    fMRI_test_IID = [fMRI_test_IID data{test_index(i_test),2}];
    if strcmp(char(data{test_index(i_test),1}) , 'AD')
        Label_test = [Label_test;zeros(length(data{test_index(i_test),2}),1)];
    else
        Label_test = [Label_test;ones(length(data{test_index(i_test),2}),1)];
    end
end
    
        
addpath(genpath('~/Zhewei/MatLabCode/'))        
%% read files in

[~,train_NC_numfiles] = size(fMRI_train_NC_IID);
lowFreq = 0.01;
hiFreq = 0.08;
fs = 1/3;
feature_No = 120;


for ifile = 1:train_NC_numfiles
    fileID = fMRI_train_NC_IID(ifile);
    cd ~/Zhewei/data/data_from_SPM/
    fMRI_train_NC{ifile,1} = fileID;
    mat_name = strcat(num2str(fMRI_train_NC_IID(ifile)), '.mat');
    feature = load(mat_name);
    feature = feature.feature;
    [m_f, n_f] = size(feature);
    tmp_feature = zeros(m_f, n_f);
    for jframe = 1:feature_No
        tmp_feature(jframe, :) = bpfilt(feature(jframe, :), lowFreq, hiFreq, fs, 0);
    end
    fMRI_train_NC{ifile,2} = tmp_feature;
    fMRI_train_NC{ifile,3} = corrcoef(tmp_feature');
 
end


for ifile = 1:train_AD_numfiles
    fileID = fMRI_train_AD_IID(ifile);
    cd ~/Zhewei/data/data_from_SPM/
    fMRI_train_AD{ifile,1} = fileID;
    mat_name = strcat(num2str(fMRI_train_AD_IID(ifile)), '.mat');
    feature = load(mat_name);
    feature = feature.feature;
    [m_f, n_f] = size(feature);
    tmp_feature = zeros(m_f, n_f);
    for jframe = 1:feature_No
        tmp_feature(jframe, :) = bpfilt(feature(jframe, :), lowFreq, hiFreq, fs, 0);
    end
    fMRI_train_AD{ifile,2} = tmp_feature;
    fMRI_train_AD{ifile,3} = corrcoef(tmp_feature');
 
end


[~,test_numfiles] = size(fMRI_test_IID);

for ifile = 1:test_numfiles
    fileID = fMRI_test_IID(ifile);
    cd ~/Zhewei/data/data_from_SPM/
    fMRI_test{ifile,1} = fileID;
    mat_name = strcat(num2str(fMRI_test_IID(ifile)), '.mat');
    feature = load(mat_name);
    feature = feature.feature;
    [m_f, n_f] = size(feature);
    tmp_feature = zeros(m_f, n_f);
    for jframe = 1:feature_No
        tmp_feature(jframe, :) = bpfilt(feature(jframe, :), lowFreq, hiFreq, fs, 0);
    end
    fMRI_test{ifile,2} = tmp_feature;
    fMRI_test{ifile,3} = corrcoef(tmp_feature');
 
end



%% Wilcoxon rank sum test
W_matrix = zeros(120,120);
for i_feature1 = 1:120
    for i_feature2 = 1:120
        % build x_NC, and y_AD
        x_NC = [];
        for ifile = 1:train_NC_numfiles
            x_NC = [x_NC fMRI_train_NC{ifile,3}(i_feature1, i_feature2)];
        end
        y_AD = [];
        for ifile = 1:train_AD_numfiles
            y_AD = [y_AD fMRI_train_AD{ifile,3}(i_feature1, i_feature2)];
        end
        
        % rank sum
        [p,h,stats] = ranksum(x_NC,y_AD);
        W_matrix(i_feature1, i_feature2) = stats.zval;
    end
end