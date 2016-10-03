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
            336551, 322009, 322000, ...
            238623, 303069, 240811, 304790, 371994, ...
            243902, 322442, 286519, 361612, 287493, ...
            361431, 254581, 273218, 290923, 335999, ...
            391150, 257271, 274579, 297353, 340048, ...
            395105, 259654, 274825, 299159, 346113, ...
            397604, 259806, 260580];
        
%% read files in

[~,numfiles] = size(fMRI_IID);
order = 10;
lowFreq = 12.5;
hiFreq = 100;
fs = 500;
feature_No = 120;


[b,a] = butter(order, [lowFreq hiFreq]/(fs/2), 'bandpass');
 %y = filter(b,a,x)

for ifile = 1:numfiles
    fileID = fMRI_IID(ifile);
    cd ~/Zhewei/data/data_from_SPM/
    mat_name = strcat(num2str(fMRI_IID(ifile)), '.mat');
    feature = load(mat_name);
    feature = feature.feature;
    [m_f, n_f] = size(feature);
    tmp_feature = zeros(m_f, n_f);
    for jframe = 1:feature_No
        tmp_feature(jframe, :) = filter(b,a, feature(jframe, :));
    end
    feature = tmp_feature;
    cd ../data_After_BandPass/
    save(mat_name, 'feature');   
    
end