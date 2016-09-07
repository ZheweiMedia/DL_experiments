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
IID = [
251176 322050 385942 274147 352947 .../
404373 227595 292427 249536 267490 .../
287274 256148 273181 293284 338109 .../
257477 274134 296652 335317 394820 .../
258528 273556 298203 285812 306320 .../
330179 363568 296366 313307 341806 .../
367496 306889 333755 352349 375097 .../
266129 266131 283851 283853 306280 .../
306277 348071 348075 269256 269253 .../
286375 286378 311356 311357 351592 .../
404475 283267 283264 283260 .../
303143 303137 334609 334605 363293 .../
303733 303731 323338 323324 348393 .../
348396 376286 339123 339129 354587 .../
371407 397506 247209 243880 260303 .../
280649 318774 381846 220070 287005 .../
363411 261166 278367 304270 324394 .../
363421 300057 325672 342309 367838 .../
339635 367161 323221 346564 361591 .../
385234 261984 277286 302671 343304 .../
415196 286477 305233 326518 362146 .../
229511 249328 265957 305277 368901 .../
235238 252282 270573 303434 360939 .../
255284 269694 286940 338318 388696 .../
255309 270542 291146 348195 391665 .../
290644 310766 417557 364453 304675 .../
328499 348153 373709 354654 .../
400360 341823 343366 259691 .../
280800 297561 342030 395958 267894 .../
287082 304596 348045 398599 287650 .../
308121 331236 362399 293629 313410 .../
341317 364929 314327 340210 355856 .../
495757 337131 352312 368186 394511 .../
332647 330141 398432 281024 330138 .../
330233 342476 375500 ];

Path = './data/LMCI_data/fMRI_%d.txt';
Path2 = './data/LMCI_data/DifferentSample.txt';


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