%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Step1: Slice timing
% Step2: Motion correction (realign & Unwarp)
% Step3: Coregistration (meand image from step2 with its own MRI, and 
%           At the same time all time frames with MRI.)
% Step4: Spatial normalization (MRI with template, and at the same time
%           all time frames with template)
% <del> Step5: Smoothing </del>
%
% Zhewei @ 9/19/2016
%
%
%
%% input image IDs
% clear all
fMRI_IID = [238623, 303069, 240811, 304790, 371994, ...
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
            268925, 297183, 321439, 401398, 266634, ...
            296891, 315798, 399633, 272223, 301492, ...
            327813, 354839, 403913, 273503, 296638, ...
            316619, 353130, 409002, 269279, 288745, ...
            306127, 347150, 401663, 315850, 338813, ...
            355339, 383452, 246871, 261918, 300743, ...
            370595, 234917, 251325, 270397, 305150, ...
            371750, 255986, 274090, 292605, 337977, ...
            391167, 280365, 302555, 321203, 282646, ...
            303248, 325233, 362235, 414942, 290815, ...
            309727, 337993, 366388, 289559, 310188, ...
            366944, 289656, 387091, 334140, 350835, ...
            348304, 350735, 353800, 266208, 289588, ...
            310240, 350046, 398573, 267713, 285316, ...
            302615, 346744, 399995, 365086, 264214, ...
            285011, 330165, 401073, 279084, 336199, ...
            308403, 308418];

MRI_IID = [238627, 303066, 240812, 304793, 371991, ...
            243898, 322437, 286516, 361610, 287487, ...
            361326, 254582, 273221, 290931, 335997, ...
            391154, 257270, 274575, 297357, 340042, ...
            395111, 259653, 274823, 299155, 346110, ...
            397601, 259796, 260581, 277128, 301756, ...
            346803, 398531, 395978, 265128, 265128, ...
            289847, 289847, 336214, 336214, 389362, ...
            268919, 268919, 286458, 286458, 311251, ...
            311251, 349323, 349323, 405713, 279470, ...
            279470, 298513, 298513, 319631, 319631, ...
            362894, 281882, 281882, 303080, 326295, ...
            326295, 361300, 337395, 363621, 283915, ...
            319212, 350451, 238532, 238532, 253529, ...
            296776, 352728, 375160, 296859, 336634, ...
            340741, 368953, 300089, 314497, 343930, ...
            368930, 308178, 262076, 296614, 320516, ...
            268930, 297182, 321444, 401399, 266625, ...
            296883, 315793, 399628, 272231, 301498, ...
            327809, 354836, 403909, 273504, 296642, ...
            316626, 353125, 408999, 269273, 288737, ...
            306125, 347158, 401656, 315857, 338816, ...
            355327, 383444, 246868, 261926, 300740, ...
            370597, 234922, 251329, 270395, 305151, ...
            371757, 255978, 274097, 292597, 337984, ...
            391177, 280369, 302554, 321197, 282638, ...
            303246, 325224, 362229, 414943, 290814, ...
            309729, 337996, 366391, 289564, 310185, ...
            366946, 289653, 387095, 334144, 350833, ...
            348300, 350736, 353802, 266217, 289591, ...
            310245, 350050, 398576, 267711, 285307, ...
            302617, 346745, 399997, 365084, 264215, ...
            285014, 330166, 401068, 278511, 336198, ...
            308396, 308415];

Path_fMRI = './data/Normal_data/fMRI_%d.txt';
Path_MRI = './data/Normal_data/MRI_%d.txt';
Path2 = './data/Normal_data/DifferentSample.txt';


%% ===================parameters at here================

% ================slice timing=========================

% number of slices is the slices in one scan, by mri_info *.nii we can get
% for fMRI it is 64*64*48, so each slice is 64*64, and 48 slices.
ST_Nslices = 48;
ST_TR = 3;
ST_TA = 3-3/48;
ST_SO = [1:1:48];
ST_Refslice = 24;
ST_prefix = '';


% ===============realign & unwarp======================
RU_pmscan = '';
RU_quality = 0.9;
RU_sep = 4;
RU_fwhm = 5;
RU_rtm = 0;
RU_einterp = 2;
RU_ewrap = [0,0,0];
RU_weight = '';
RU_basfcn = [12,12];
RU_regorder = 1;
RU_lambda = 100000;
RU_jm = 0;
RU_fot = [4,5];
RU_sot = [];
RU_uwfwhm = 4;
RU_rem = 1;
RU_noi = 5;
RU_expround = 'Average';
RU_uwwhich = [2,1];
RU_rinterp = 4;
RU_wrap = [0,0,0];
RU_mask = 1;
RU_prefix = '';

% ===================coregistration====================

CO_cost_fun = 'nmi';
CO_sep = [4,2];
CO_tol = [0.0200,0.0200,0.0200, 1.0000e-03, 1.0000e-03, 1.000e-03, ...
        0.0100, 0.0100, 0.0100, 1.0000e-03, 1.0000e-03, 1.000e-03];

CO_fwhm = [7,7];
CO_interp = 4;
CO_wrap = [0,0,0];
CO_mask = 0;
CO_prefix = '';

% ====================Normalise========================
% normalize with the MNI space, avg152T1.nii
Nor_biasreg = 1.0000e-04;
Nor_biasfwhm = 60;
Nor_eoptions_tpm = {'/home/medialab/spm12/tpm/TPM.nii'};
Nor_eoptions_affreg = 'mni';
Nor_eoptions_reg = [0 1.0000e-03 0.5 0.05 0.2];
Nor_fwhm = 0;
Nor_samp = 3;
Nor_bb = [-90 -126 -72;90 90 108];
Nor_vox = [2 2 2];
Nor_interp = 4;
Nor_prefix = '';
% 
% % ======================Smooth=========================
% SM_fwhm = [8 8 8];
% SM_dtype = 0;
% SM_im = 0;
% SM_prefix = '';

%% ===================Parameters Done========================

% Read links files for fMRI, MRI, and mean,
[~,numfiles] = size(fMRI_IID);
fMRI_data = cell(1, numfiles);
MRI_data = cell(1,numfiles);
mean_data = cell(1,numfiles);

% for fMRI
for ifile = 1:numfiles
    fileID = fMRI_IID(ifile);
    IIDfilename = sprintf(Path_fMRI, fileID);
    fMRI_data{ifile} = sort(importdata(IIDfilename));
end

% for MRI
for ifile = 1:numfiles
    fileID = MRI_IID(ifile);
    IIDfilename = sprintf(Path_MRI, fileID);
    MRI_data{ifile} = sort(importdata(IIDfilename));
end

% for mean
for ifile = 1:numfiles
    [file_dir, file_name, file_postFix] = fileparts(fMRI_data{ifile}{11});
    means_name = strcat('/mean',file_name);
    mean_data{ifile}{1} = strcat(file_dir,means_name,file_postFix);
end

% some modification to fit SPM12
% ================================

fMRI_data = ADD_one(fMRI_data);
MRI_data = ADD_one(MRI_data);
mean_data = ADD_one(mean_data);

% start to work automatically
fileWrite = fopen(Path2,'w');

for ifile = 1:numfiles
    
    img_data = sort([fMRI_data{1,ifile}]);
    img_data = img_data(11:140);
    %% =================Slice Timing===============================
    display('Slice Timing..........................................')
    % build the job structure of slice timing
    job.scans = {img_data};
    job.nslices = ST_Nslices;
    job.tr = ST_TR;
    job.ta = ST_TA;
    job.so = ST_SO;
    job.refslice = ST_Refslice;
    job.prefix = ST_prefix;
    % ========================different samples====================
%     P = cell(size(job.scans));
%     for i = 1:numel(job.scans)
%         P{i} = char(job.scans{i});
%     end
%     Vin     = spm_vol(P{1}(1,:));
%     nslices = Vin(1).dim(3);
%     if nslices ~= numel(job.so)
%         fprintf(fileWrite,'%d\n',IID(ifile));
%         fprintf(fileWrite,'%d\n',nslices);
%         continue
%     end
    % ==============================================================
    
    spm_run_st(job);
    clearvars job;
    %% ===================Realign & Unwarp==========================
    display('Realign & Unwarp..........................................')
    job.data.scans = {img_data};
    job.data.pmscan = RU_pmscan;
    job.eoptions.quality = RU_quality;
    job.eoptions.sep = RU_sep;
    job.eoptions.fwhm = RU_fwhm;
    job.eoptions.rtm = RU_rtm;
    job.eoptions.einterp = RU_einterp;
    job.eoptions.ewrap = RU_ewrap;
    job.eoptions.weight = RU_weight;
    job.uweoptions.basfcn = RU_basfcn;
    job.uweoptions.regorder = RU_regorder;
    job.uweoptions.lambda = RU_lambda;
    job.uweoptions.jm = RU_jm;
    job.uweoptions.fot = RU_fot;
    job.uweoptions.sot = RU_sot;
    job.uweoptions.uwfwhm = RU_uwfwhm;
    job.uweoptions.rem = RU_rem;
    job.uweoptions.noi = RU_noi;
    job.uweoptions.expround = RU_expround;
    job.uwroptions.uwwhich = RU_uwwhich;
    job.uwroptions.rinterp = RU_rinterp;
    job.uwroptions.wrap = RU_wrap;
    job.uwroptions.mask = RU_mask;
    job.uwroptions.prefix = RU_prefix;
    spm_run_realignunwarp(job);
    clearvars job;
    %% =======================Coregistration=======================
          
    display('Coregistration..........................................')
    job.ref = MRI_data{ifile};
    job.source = mean_data{ifile};
    job.other = img_data;
    job.eoptions.cost_fun = CO_cost_fun;
    job.eoptions.sep = CO_sep;
    job.eoptions.tol = CO_tol;
    job.eoptions.fwhm = CO_fwhm;
    job.roptions.interp = CO_interp;
    job.roptions.wrap = CO_wrap;
    job.roptions.mask = CO_mask;
    job.roptions.prefix = CO_prefix;
    spm_run_coreg(job);

    %% ======================Spatial Normalization===================
    job.subj.vol = MRI_data{ifile};
    job.subj.resample = {img_data};
    job.eoptions.biasreg = Nor_biasreg;
    job.eoptions.biasfwhm = Nor_biasfwhm;
    job.eoptions.tpm = Nor_eoptions_tpm;
    job.eoptions.affreg = Nor_eoptions_affreg;
    job.eoptions.reg = Nor_eoptions_reg;
    job.eoptions.fwhm = Nor_fwhm;
    job.eoptions.samp = Nor_samp;
    job.woptions.bb = Nor_bb;
    job.woptions.vox = Nor_vox;
    job.woptions.interp = Nor_interp;
    job.woptions.prefix = Nor_prefix;
    spm_run_norm(job);
    clearvars job;   
    
    
%     %% =========================Smoothing===============================
%     varargin{1,1}.data = {img_data};
%     varargin{1,1}.fwhm = SM_fwhm;
%     varargin{1,1}.dtype = SM_dtype;
%     varargin{1,1}.im = SM_im;
%     varargin{1,1}.prefix = SM_prefix;
%     spm_run_smooth(varargin);
%     clearvars varargin;

    
    
end







