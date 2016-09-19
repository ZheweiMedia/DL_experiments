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
fMRI_IID = [238623, 303069, 240811, 371994, 304790, 243902, ...
        322442, 286519, 361612, 287493, 361431, 254581, ...
        273218, 391150, 335999, 290923, 257271, 395105, ...
        340048, 274579, 297353, 259654, 299159, 346113, ...
        397604, 274825, 259806, 260580, 346801, 277135, ...
        301757, 398533, 395980, 265132, 265125, 336212, ...
        389367, 336216, 289854, 289846, 268914, 286464, ...
        286461, 349320, 405706, 311257, 311258, 268917, ...
        349326, 279468, 298515, 279472, 362889, 319632, ...
        319634, 298510, 281881, 303083, 281887, 326301, ...
        326298, 361294, 337404, 363620, 283913, 350450, ...
        319211, 238540, 238542, 253525, 296769, 352724, ...
        375151, 296863, 368950, 369618, 340743, 300088, ...
        314505, 343935, 368923, 308182, 262078, 296612, ...
        320519, 268925, 321439, 297183, 401398, 266634, ...
        296891, 399633, 315798, 272223, 327813, 354839, ...
        403913, 301492, 273503, 296638, 409002, 353130, ...
        316619, 269279, 347150, 401663, 288745, 306127, ...
        315850, 383452, 355339, 338813, 370595, 246871, ...
        300743, 261918, 234917, 305150, 251325, 270397, ...
        371750, 255986, 391167, 337977, 274090, 292605, ...
        280365, 321203, 302555, 282646, 325233, 303248, ...
        414942, 362235, 290815, 337993, 366388, 309727, ...
        289559, 366944, 310188, 289656, 387091, 334140, ...
        350835, 348304, 350735, 353800, 266208, 350046, ...
        398573, 310240, 289588, 267713, 302615, 346744, ...
        285316, 399995, 365086, 264214, 285011, 401073, ...
        330165, 279084, 336199, 308403, 308418];

MRI_IID = [];

Path = './data/Normal_data/fMRI_%d.txt';
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
CO_ref =  11%;
CO_source = 22%MRI nii%
CO_other = 33%fMRI%
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
Nor_eoptions_tpm = {'/home/medialab/spm12/canonical/avg152T1.nii'};
Nor_eoptions_affreg = 'mni';
Nor_eoptions_reg = [0 1.0000e-03 0.5 0.05 0.2];
Nor_fwhm = 0;
Nor_samp = 3;
Nor_bb = [-78 -112 -70;78 76 85];
Nor_vox = [2 2 2];
Nor_interp = 4;
Nor_prefix = 't';
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

for ifile = 1:numfiles
    fileID = fMRI_IID(ifile);
    IIDfilename = sprintf(Path, fileID);
    
    fMRI_data{ifile} = importdata(IIDfilename);    
end

% some modification to fit SPM12
% ================================

for ifile = 1:numfiles
    [rows, col] = size(fMRI_data{1,ifile});
    for irow = 1:rows
        fMRI_data{1,ifile}{irow,col} = strcat(fMRI_data{1,ifile}{irow,col},',1');
    end
end


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
    job.ref = CO_ref;
    job.source = img_data(1);
    job.other = img_data(2:end);
    job.eoptions.cost_fun = CO_cost_fun;
    job.eoptions.sep = CO_sep;
    job.eoptions.tol = CO_tol;
    job.eoptions.fwhm = CO_fwhm;
    job.roptions.interp = CO_interp;
    job.roptions.wrap = CO_wrap;
    job.roptions.mask = CO_mask;
    job.roptions.prefix = CO_prefix;
    spm_run_coreg(job);

%     %% ======================Spatial Normalization===================
%     job.subj.vol = img_data(1);
%     job.subj.resample = img_data;
%     job.eoptions.biasreg = Nor_biasreg;
%     job.eoptions.biasfwhm = Nor_biasfwhm;
%     job.eoptions.tpm = Nor_eoptions_tpm;
%     job.eoptions.affreg = Nor_eoptions_affreg;
%     job.eoptions.reg = Nor_eoptions_reg;
%     job.eoptions.fwhm = Nor_fwhm;
%     job.eoptions.samp = Nor_samp;
%     job.woptions.bb = Nor_bb;
%     job.woptions.vox = Nor_vox;
%     job.woptions.interp = Nor_interp;
%     job.woptions.prefix = Nor_prefix;
%     spm_run_norm(job);
%     clearvars job;   
%     
%     
%     %% =========================Smoothing===============================
%     varargin{1,1}.data = {img_data};
%     varargin{1,1}.fwhm = SM_fwhm;
%     varargin{1,1}.dtype = SM_dtype;
%     varargin{1,1}.im = SM_im;
%     varargin{1,1}.prefix = SM_prefix;
%     spm_run_smooth(varargin);
%     clearvars varargin;

    
    
end



clear all;





%% input image IDs
% clear all
fMRI_IID = [346237, 372812, 398684, 358614, 293808, 335306, ...
        293809, 264987, 390346, 264986, 335307, 258600, ...
        272411, 340024, 272407, 302042, 258605, 302039, ...
        393209, 340021, 287992, 310925, 310931, 336551, ...
        287986, 336552, 322000, 362021, 346367, 346359, ...
        394330, 322009, 360323, 373417, 390453, 301395, ...
        343571, 321520, 306073, 327941, 348646, 360317, ...
        382187, 258955, 300352, 396527, 396530, 272535, ...
        341972, 280778, 359770, 412884, 297106, 322347, ...
        300334, 317435, 343285, 363190, 343912, 400431, ...
        372599, 358050, 345555, 372471, 358811, 415205, ...
        228872, 248870, 297847, 263860, 357475, 415178, ...
        372254, 389296, 376933, 368413, 291229, 347092, ...
        323796, 295969, 367094, 342048, 316009, 300043, ...
        369943, 322371, 342223, 306375, 352396, 335235, ...
        376259, 342326, 370085, 358899, 341793, 369299, ...
        395989, 358857, 342278, 353265, 392395, 364935, ...
        342915, 369264, 347402, 348491, 398911, 360702, ...
        373027, 358777, 371972, 385034, 381307, 367567, ...
        379705, 342514];

Path = './data/AD_data/fMRI_%d.txt';
Path2 = './data/AD_data/DifferentSample.txt';


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

% % ====================Normalise========================
% % normalize with the MNI space, avg152T1.nii
% Nor_biasreg = 1.0000e-04;
% Nor_biasfwhm = 60;
% Nor_eoptions_tpm = {'/home/medialab/spm12/canonical/avg152T1.nii'};
% Nor_eoptions_affreg = 'mni';
% Nor_eoptions_reg = [0 1.0000e-03 0.5 0.05 0.2];
% Nor_fwhm = 0;
% Nor_samp = 3;
% Nor_bb = [-78 -112 -70;78 76 85];
% Nor_vox = [2 2 2];
% Nor_interp = 4;
% Nor_prefix = 't';
% 
% % ======================Smooth=========================
% SM_fwhm = [8 8 8];
% SM_dtype = 0;
% SM_im = 0;
% SM_prefix = '';

% ===================coregistration====================
CO_ref = {'/home/medialab/spm12/canonical/avg152T1.nii,1'};
CO_cost_fun = 'nmi';
CO_sep = [4,2];
CO_tol = [0.0200,0.0200,0.0200, 1.0000e-03, 1.0000e-03, 1.000e-03, 
        0.0100, 0.0100, 0.0100, 1.0000e-03, 1.0000e-03, 1.000e-03];


CO_fwhm = [7,7];
CO_interp = 4;
CO_wrap = [0,0,0];
CO_mask = 0;
CO_prefix = '';

%% ===================Parameters Done========================

[~,numfiles] = size(fMRI_IID);
fMRI_data = cell(1, numfiles);

for ifile = 1:numfiles
    fileID = fMRI_IID(ifile);
    IIDfilename = sprintf(Path, fileID);
    
    fMRI_data{ifile} = importdata(IIDfilename);    
end

% some modification to fit SPM12
% ================================

for ifile = 1:numfiles
    [rows, col] = size(fMRI_data{1,ifile});
    for irow = 1:rows
        fMRI_data{1,ifile}{irow,col} = strcat(fMRI_data{1,ifile}{irow,col},',1');
    end
end


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
    

%     %% ======================Spatial Normalization===================
%     job.subj.vol = img_data(1);
%     job.subj.resample = img_data;
%     job.eoptions.biasreg = Nor_biasreg;
%     job.eoptions.biasfwhm = Nor_biasfwhm;
%     job.eoptions.tpm = Nor_eoptions_tpm;
%     job.eoptions.affreg = Nor_eoptions_affreg;
%     job.eoptions.reg = Nor_eoptions_reg;
%     job.eoptions.fwhm = Nor_fwhm;
%     job.eoptions.samp = Nor_samp;
%     job.woptions.bb = Nor_bb;
%     job.woptions.vox = Nor_vox;
%     job.woptions.interp = Nor_interp;
%     job.woptions.prefix = Nor_prefix;
%     spm_run_norm(job);
%     clearvars job;   
%     
%     
%     %% =========================Smoothing===============================
%     varargin{1,1}.data = {img_data};
%     varargin{1,1}.fwhm = SM_fwhm;
%     varargin{1,1}.dtype = SM_dtype;
%     varargin{1,1}.im = SM_im;
%     varargin{1,1}.prefix = SM_prefix;
%     spm_run_smooth(varargin);
%     clearvars varargin;
      %% =======================Coregistration=======================
    display('Coregistration..........................................')
    job.ref = CO_ref;
    job.source = img_data(1);
    job.other = img_data(2:end);
    job.eoptions.cost_fun = CO_cost_fun;
    job.eoptions.sep = CO_sep;
    job.eoptions.tol = CO_tol;
    job.eoptions.fwhm = CO_fwhm;
    job.roptions.interp = CO_interp;
    job.roptions.wrap = CO_wrap;
    job.roptions.mask = CO_mask;
    job.roptions.prefix = CO_prefix;
    spm_run_coreg(job);
    
    
end