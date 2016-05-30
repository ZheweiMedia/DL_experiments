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
213885 180734 199148 243875 316041 ...\
381524 191820 207955 256635 223330 ...\
192250 207666 257487 332881 393007 ...\
258448 279226 301767 346233 395573 ...\
278818 300245 323843 361436 414381 ...\
283879 305240 326318 358424 417987 ...\
311921 332859 354814 379008 307555 ...\
307553 334236 334235 350115 350113 ...\
381403 246032 265869 306576 372938 ...\
248233 265533 290438 336704 385092 ...\
255318 274437 301834 393850 319132 ...\
376489 361973 388039 343905 361116 ...\
372823 398098 261316 261319 225058 ...\
242252 305412 286425 241661 257106 ...\
339828 264416 281497 308391 347747 ...\
320432 337377 352722 367848 332584 ...\
347725 364273 390419 252603 199197 ...\
224635 280337 352437 402257 255135 ...\
202425 226625 243008 207341 222174 ...\
274112 351336 399918 247852 207991 ...\
223649 281032 353098 404042 290305 ...\
321928 362541 311906 338289 353986 ...\
378012 319541 346592 358601 386888 ...\
260905 277297 301221 341866 398232 ...\
300529 316049 343137 370437 183884 ...\
215435 181505 193431 242177 310476 ...\
379344 217608 184535 196434 247662 ...\
316979 382683 240043 208974 223353 ...\
275532 354598 226190 243115 259900 ...\
297463 367820 249144 264701 284291 ...\
329780 387206 281149 299318 324478 ...\
357940 339436 354860 367326 394943 ...\
401558 264531 228463 245122 305210 ...\
374515 283305 247533 267918 319578 ...\
382880 289331 307991 337186 306672 ...\
333641 376324 316519 337220 354697 ...\
383934 235258 298266 317378 344443 ...\
377061 300841 316406 347906 375664 ...\
361367 317397 336187 266223 232243 ...\
247983 302589 372302  240902 ...\
257011 316276 385078 256753 297616 ...\
259332 281083 341127 394175 279103 ...\
297702 374201 358935 412933 278493 ...\
305261 374165 374144 407059 279181 ...\
301103 319553 358798 414279 282297 ...\
303032 323821 361486 323163 ...\
349748 374318 392890 293995 ...\
341976  ];

Path = './data/EMCI_data/fMRI_%d.txt';


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
fileWrite = fopen('DifferentSample.txt','w');

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