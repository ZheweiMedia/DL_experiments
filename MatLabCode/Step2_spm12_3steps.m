%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%
%
%
%
%
%
%% input image IDs
% clear all
IID = [346237, 372812, 398684, 358614, 248516, 390346, 264986, ...
        293809, 293808, 335306, 335307, 264987, 258600, 272407, ...
        393209, 340021, 340024, 258605, 272411, 302042, 302039, ...
        287992, 310925, 287986, 336552, 310931, 336551, 322000, ...
        322009, 346359, 362021, 346367, 394330, 375331, 360323, ...
        373417, 390453, 301395, 321520, 343571, 306073, 348646, ...
        327941, 360317, 382187, 258955, 341972, 272535, 300352, ...
        396527, 396530, 280778, 322347, 297106, 412884, 359770, ...
        300334, 343285, 363190, 317435, 343912, 400431, 372599, ...
        358050, 345555, 372471, 358811, 415205, 228872, 248870, ...
        263860, 297847, 357475, 415178, 372254, 389296, 376933, ...
        368413, 291229, 323796, 347092, 295969, 342048, 367094, ...
        316009, 300043, 342223, 322371, 369943, 306375, 335235, ...
        352396, 376259, 342326, 358899, 370085, 341793, 358857, ...
        369299, 395989, 342278, 353265, 392395, 364935, 342915, ...
        369264, 347402, 348491, 373027, 398911, 360702, 358777, ...
        385034, 371972, 381307, 367567, 379705, 342514 ];

Path = './data/AD_data/fMRI_%d.txt';
Path2 = './data/AD_data/DifferentSample.txt';


%===========parameters at here================

% number of slices is the slices in one scan, by mri_info *.nii we can get
% for fMRI it is 64*64*48, so each slice is 64*64, and 48 slices.
ST_Nslices = 48;
ST_TR = 3;
ST_TA = 3-3/48;
ST_SO = [1:1:48];
ST_Refslice = 24;
ST_prefix = '';


% realign & unwarp
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

% coregistration
CO_ref = {'/home/medialab/spm12/atlas/AAL2.nii,1'};
CO_cost_fun = 'nmi';
CO_sep = [4,2];
CO_tol = [0.0200,0.0200,0.0200, 1.0000e-03, 1.0000e-03, 1.000e-03, 
        0.0100, 0.0100, 0.0100, 1.0000e-03, 1.0000e-03, 1.000e-03];


CO_fwhm = [7,7];
CO_interp = 4;
CO_wrap = [0,0,0];
CO_mask = 0;
CO_prefix = '';

%=============================================

[~,numfiles] = size(IID);
data = cell(1, numfiles);

for ifile = 1:numfiles
    fileID = IID(ifile);
    IIDfilename = sprintf(Path, fileID);
    
    data{ifile} = importdata(IIDfilename);    
end

% some modification to fit SPM12
% ================================

for ifile = 1:numfiles
    [rows, col] = size(data{1,ifile});
    for irow = 1:rows
        data{1,ifile}{irow,col} = strcat(data{1,ifile}{irow,col},',1');
    end
end


% start to work automatically
fileWrite = fopen(Path2,'w');

for ifile = 1:numfiles
    
    img_data = sort([data{1,ifile}]);
    img_data = img_data(11:140);
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
    P = cell(size(job.scans));
    for i = 1:numel(job.scans)
        P{i} = char(job.scans{i});
    end
    Vin     = spm_vol(P{1}(1,:));
    nslices = Vin(1).dim(3);
    if nslices ~= numel(job.so)
        fprintf(fileWrite,'%d\n',IID(ifile));
        fprintf(fileWrite,'%d\n',nslices);
        continue
    end
    % ==============================================================
    
    spm_run_st(job);
    clearvars job;
    display('Realign & Unwarp..........................................')
    job.data.scans = img_data;
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