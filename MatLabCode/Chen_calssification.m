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



load('dataList.mat')

cd ~/Zhewei/data/data_from_SPM/

% subjects: 48
subjectNo = 48;
index = randperm(subjectNo);
train_index = index(1:45);
test_index = index(46:end);

fMRI_train_NC_IID = [];
fMRI_train_AD_IID = [];
fMRI_test_IID = [];
label_test = [];
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
        label_test = [label_test;zeros(length(data{test_index(i_test),2}),1)];
    else
        label_test = [label_test;ones(length(data{test_index(i_test),2}),1)];
    end
end
    
        
addpath(genpath('~/Zhewei/MatLabCode/'))        
%% read files in, { , 2} is the signal after filter, { , 3} is the r matrix.

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

[~,train_AD_numfiles] = size(fMRI_train_AD_IID);
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


%% find out the features
% How to decide the features? increase connection set and decreased
% connection set. choose 100 for each set.

w_M_copy1 = W_matrix;
Select_feature = 5;
increase_index = [];
for i = 1:Select_feature*2
    [row_value, row_index] = max(w_M_copy1);
    [max_value, column_index] = max(row_value);
    increase_index = [increase_index;[row_index(column_index) column_index]];
    % reduce the value and make it be negative inf
    w_M_copy1(row_index(column_index), column_index) = -Inf;
    
end

w_M_copy2 = W_matrix;
decrease_index = [];
for i = 1:Select_feature*2
    [row_value, row_index] = min(w_M_copy2);
    [min_value, column_index] = min(row_value);
    decrease_index = [decrease_index;[row_index(column_index) column_index]];
    % reduce the value and make it be negative inf
    w_M_copy2(row_index(column_index), column_index) = Inf;
    
end

% remove the duplicate index
increase_set = [];
for i  = 1:2:Select_feature*2
    increase_set = [increase_set; increase_index(i,:)];
end

decrease_set = [];
for i  = 1:2:Select_feature*2
    decrease_set = [decrease_set; decrease_index(i,:)];
end


%% Now let's build the classifier

% feature of NC
feature_NC = [];
label_NC = [];
for i = 1:train_NC_numfiles
    tmp_feature = [];
    % increase set feature
    for j = 1:Select_feature
        tmp_feature = [tmp_feature fMRI_train_NC{i,3}(increase_set(j,1), increase_set(j,2))];
    end
    % decrease set feature
    for j = 1:Select_feature
        tmp_feature = [tmp_feature fMRI_train_NC{i,3}(decrease_set(j,1), decrease_set(j,2))];
    end
        
    % put in feature matrix
    feature_NC = [feature_NC;tmp_feature];
    label_NC = [label_NC; 1];
end


% feature of AD
feature_AD = [];
label_AD = [];
for i = 1:train_AD_numfiles
    tmp_feature = [];
    % increase set feature
    for j = 1:Select_feature
        tmp_feature = [tmp_feature fMRI_train_AD{i,3}(increase_set(j,1), increase_set(j,2))];
    end
    % decrease set feature
    for j = 1:Select_feature
        tmp_feature = [tmp_feature fMRI_train_AD{i,3}(decrease_set(j,1), decrease_set(j,2))];
    end
        
    % put in feature matrix
    feature_AD = [feature_AD;tmp_feature];
    label_AD = [label_AD; 0];
end

% feature of test
feature_test = [];
for i = 1:test_numfiles
    tmp_feature = [];
    % increase set feature
    for j = 1:Select_feature
        tmp_feature = [tmp_feature fMRI_test{i,3}(increase_set(j,1), increase_set(j,2))];
    end
    % decrease set feature
    for j = 1:Select_feature
        tmp_feature = [tmp_feature fMRI_test{i,3}(decrease_set(j,1), decrease_set(j,2))];
    end
        
    % put in feature matrix
    feature_test = [feature_test;tmp_feature];
end


%   SVM classifier

trainData = [feature_NC;feature_AD];
trainLabel = [label_NC; label_AD];

% MD = fitcsvm(trainData,trainLabel,'Standardize',false,'KernelFunction','RBF','KernelScale','auto');
MD = fitcdiscr(trainData,trainLabel, 'discrimType','pseudoLinear');
test_pred = predict(MD, feature_test);
sum((label_test == test_pred))/length(label_test)