%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%   1. Set data ID, data, in cells.
%   2. Pearson corelation, also store in cells.
%
%
%
%




clear all


fMRI_NC_IID = [346237, 358614, 372812, 398684, 264986, ...
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
            342223, 369943, 306375, 335235, 352396, ...
            ];
fMRI_AD_IID = [238623, 303069, 240811, 304790, 371994, ...
            243902, 322442, 286519, 361612, 287493, ...
            361431, 254581, 273218, 290923, 335999, ...
            391150, 257271, 274579, 297353, 340048, ...
            395105, 259654, 274825, 299159, 346113, ...
            397604, 259806, 260580, 277135, 301757, ...
            346801, 398533, 395980, 265132, 265125, ...
            289854, 289846, 336212, 336216, 389367, ...
            268917, 268914, 286461, 286464, 311257, ...
            311258, 349326, 349320, 405706, 279468, ...
            279472, 298510, 298515, 319634, 319632, ...
            362889, 281881, 281887, 303083, 326301, ...
            326298, 361294, 337404, 363620, 283913, ... 
            319211, 350450, 238540, 238542, 253525, ...
            296769, 352724, 375151, 296863, 369618, ...
            340743, 368950, 300088, 314505, 343935, ...
            368923, 308182, 262078, 296612, 320519, ...
            268925, 297183, 321439, 401398, 266634];
        
addpath(genpath('~/Zhewei/MatLabCode/'))        
%% read files in

[~,NC_numfiles] = size(fMRI_NC_IID);
lowFreq = 0.02;
hiFreq = 0.08;
fs = 1/3;
feature_No = 120;

NC_corr = zeros(120, 120);
for ifile = 1:NC_numfiles
    fileID = fMRI_NC_IID(ifile);
    cd ~/Zhewei/data/data_from_Nitime/
    fMRI_NC{ifile,1} = fileID;
    mat_name = strcat(num2str(fMRI_NC_IID(ifile)), '.mat');
    feature = load(mat_name);
    feature = feature.feature;
    [m_f, n_f] = size(feature);
    tmp_feature = zeros(m_f, n_f);
    for jframe = 1:feature_No
        tmp_feature(jframe, :) = bpfilt(feature(jframe, :), lowFreq, hiFreq, fs, 0);
        tmp_feature(jframe, :) = tmp_feature(jframe, :) - mean(tmp_feature(jframe, :)) + mean(feature(jframe, :));
    end
    fMRI_NC{ifile,2} = tmp_feature;
    fMRI_NC{ifile,3} = corrcoef(tmp_feature'); 
end


[~,AD_numfiles] = size(fMRI_AD_IID);

AD_corr = zeros(120, 120);
for ifile = 1:AD_numfiles
    fileID = fMRI_AD_IID(ifile);
    cd ~/Zhewei/data/data_from_Nitime/
    fMRI_AD{ifile,1} = fileID;
    mat_name = strcat(num2str(fMRI_AD_IID(ifile)), '.mat');
    feature = load(mat_name);
    feature = feature.feature;
    [m_f, n_f] = size(feature);
    tmp_feature = zeros(m_f, n_f);
    for jframe = 1:feature_No
        tmp_feature(jframe, :) = bpfilt(feature(jframe, :), lowFreq, hiFreq, fs, 0);
        tmp_feature(jframe, :) = tmp_feature(jframe, :) - mean(tmp_feature(jframe, :)) + mean(feature(jframe, :));
    end
    fMRI_AD{ifile,2} = tmp_feature;
    fMRI_AD{ifile,3} = corrcoef(tmp_feature');
 
end



%% Wilcoxon rank sum test
W_matrix = zeros(120,120);
for i_feature1 = 1:120
    for i_feature2 = 1:120
        % build x_NC, and y_AD
        x_NC = [];
        for ifile = 1:NC_numfiles
            x_NC = [x_NC fMRI_NC{ifile,3}(i_feature1, i_feature2)];
        end
        y_AD = [];
        for ifile = 1:AD_numfiles
            y_AD = [y_AD fMRI_AD{ifile,3}(i_feature1, i_feature2)];
        end
        
        % rank sum
        [p,h,stats] = ranksum(x_NC,y_AD);
        W_matrix(i_feature1, i_feature2) = stats.zval;
    end
end


%% histogram
connectList = [];
for i_feature1 = 1:120
    for i_feature2 = 1:i_feature1
        connectList = [connectList W_matrix(i_feature1, i_feature2)];
    end
end

% histogram(connectList)


w_M_copy1 = W_matrix;
Select_feature = 50;
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




            
        
        


