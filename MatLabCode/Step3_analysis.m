%%
% 05/27/2016
%
%

% clear all

%%

%%
IID = [ 346237 358614 372812 398684 248516 ...\
264986 264987 293808 293809 335307 ...\
335306 390346 258600 258605 272407 ...\
272411 302039 302042 340021 340024 ...\
393209 287986 287992 310931 310925 ...\
336551 336552 322000 322009 346359 ...\
346367 362021 394330 375331 360323 ...\
373417 390453 301395 321520 343571 ...\
306073 327941 348646 360317 382187 ...\
258955 272535 300352 341972 396527 ...\
396530 280778 297106 322347 359770 ...\
412884 300334 317435 343285 363190 ...\
343912 358050 372599 400431 345555 ...\
358811 372471 415205 228872 248870 ...\
263860 297847 357475 372254 389296 ...\
415178 376933 368413 291229 323796 ...\
347092 295969 316009 342048 367094 ...\
300043 322371 342223 369943 306375 ...\
335235 352396 376259 342326 358899 ...\
370085 341793 358857 369299 395989 ...\
342278 353265 364935 392395 342915 ...\
369264 347402 348491 360702 373027 ...\
398911 358777 371972 385034 381307 ...\
367567 379705 342514  ];

path_ToFile = './data/AD_data/fMRI_%d.txt';
path_ToResult = '/home/medialab/Zhewei/MatLabCode/data/LMCI_data/LM_Result%d.txt';


lenthOfFMRI = 130;


%% index of AAL2
[index, Label, value] = textread('/home/medialab/spm12/atlas/aal2.nii.txt','%u %s %u');
% then make a dictionary
[i_index,~] = size(index);
dictionary = zeros(i_index, 2);% map index and value
dictionary(:,1) = index;
dictionary(:,2) = value;


%%
[~,numfiles] = size(IID);
data = cell(1, numfiles);

for iifile = 1:numfiles
    fileID = IID(iifile);
    IIDfilename = sprintf(path_ToFile, fileID);

    IID_data = importdata(IIDfilename);
    IID_data = sort(IID_data);
    IID_data = IID_data(11:140);

    data{iifile} = IID_data;
end

%% find global min and global max
global_min = [];
global_max = [];
for ifile = 1:numfiles
    display(ifile);
    for ii = 1:lenthOfFMRI
        frame = data{1,ifile}{ii,1};
        nii_fMRI = load_untouch_nii(frame);
        img = double(nii_fMRI.img);
        local_min = min(min(min(img)));
        local_max = max(max(max(img)));
        global_min = [local_min global_min];
        global_max = [local_max global_max];
    end

end

global_min = min(min(global_min));
global_max = max(max(global_max));
% global_min = -1055;
% global_max = 5032;

%% iterate on fMRI

% open a file, write data in it


parfor ifile = 1:numfiles
    
    IIDfilename = sprintf(path_ToResult, IID(ifile));
    fileWrite = fopen(IIDfilename,'w');


    fprintf(fileWrite,'===========%d================\n',IID(ifile));
    display(ifile);

    nii_atlas = load_untouch_nii('/home/medialab/spm12/atlas/AAL2.nii');% atlas
    [x,y,z] = size(nii_atlas.img);

    for ii = 1:lenthOfFMRI
        frame = data{1,ifile}{ii,1};
        % # Should sort at here
        fid = fopen(frame);
        fprintf(fileWrite,'========================%d===============\n',ii+10);
        display(ii)


        nii_fMRI = load_untouch_nii(frame);% fMRI images

        % empty table, index, sum of intensities, and #of intensities, average
        % value

        statist_table = zeros(i_index, 4);

        % iterate
        %

        test = [];
        for i = 1:x
            for j = 1:y
                for k = 1:z
                    index_intensity = find(nii_atlas.img(i,j,k)==dictionary(:,2));
                    if ~isempty(index_intensity)
                        statist_table(index_intensity,3) = statist_table(index_intensity,3)+1;
                        pixel = (double(nii_fMRI.img(i,j,k))-global_min)/(global_max-global_min);
                        statist_table(index_intensity,2) = statist_table(index_intensity,2)+pixel;
                    end
                end
            end
        end

        for i = 1:i_index
            if statist_table(i,3)~=0
                statist_table(i,4) = statist_table(i,2)/statist_table(i,3);
            end
        end


        fprintf(fileWrite,'%8f\r\n',statist_table(:,4));

    end


end
