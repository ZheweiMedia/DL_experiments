%%
% 05/27/2016
%
%

% clear all

%%

%%
IID = [ 251176 322050 385942 274147 352947 ...\
404373 227595 292427 249536 267490 ...\
287274 256148 273181 293284 338109 ...\
257477 274134 296652 335317 394820 ...\
258528 273556 298203 285812 306320 ...\
330179 363568 296366 313307 341806 ...\
367496 306889 333755 352349 375097 ...\
266129 266131 283851 283853 306280 ...\
306277 348071 348075 269256 269253 ...\
286375 286378 311356 311357 351592 ...\
404475 283267 283264 283260 ...\
303143 303137 334609 334605 363293 ...\
303733 303731 323338 323324 348393 ...\
348396 376286 339123 339129 354587 ...\
371407 397506 247209 243880 260303 ...\
280649 318774 381846 220070 287005 ...\
363411 261166 278367 304270 324394 ...\
363421 300057 325672 342309 367838 ...\
339635 367161 323221 346564 361591 ...\
385234 261984 277286 302671 343304 ...\
415196 286477 305233 326518 362146 ...\
229511 249328 265957 305277 368901 ...\
235238 252282 270573 303434 360939 ...\
255284 269694 286940 338318 388696 ...\
255309 270542 291146 348195 391665 ...\
290644 310766 417557 364453 304675 ...\
328499 348153 373709 354654 ...\
400360 341823 343366 259691 ...\
280800 297561 342030 395958 267894 ...\
287082 304596 348045 398599 287650 ...\
308121 331236 362399 293629 313410 ...\
341317 364929 314327 340210 355856 ...\
495757 337131 352312 368186 394511 ...\
332647 330141 398432 281024 330138 ...\
330233 342476 375500  ];

path_ToFile = './data/LMCI_data/fMRI_%d.txt';
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
