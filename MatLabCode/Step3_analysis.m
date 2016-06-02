%%
% 05/27/2016
%
%

% clear all

%%

%%
IID = [ 243875 316041 ...\
381524  256635 223330 ...\
 257487 332881 393007 ...\
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
347725 364273 390419 252603  ...\
224635 280337 352437 402257 255135 ...\
226625 243008 207341 222174 ...\
274112 351336 399918 247852 207991 ...\
223649 281032 353098 404042 290305 ...\
321928 362541 311906 338289 353986 ...\
378012 319541 346592 358601 386888 ...\
260905 277297 301221 341866 398232 ...\
300529 316049 343137 370437 ...\
215435 242177 310476 ...\
379344 217608 196434 247662 ...\
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
361367 317397 336187 266223 ...\
247983 302589 372302 240902 ...\
257011 316276 385078 256753 297616 ...\
259332 281083 341127 394175 279103 ...\
297702 374201 358935 412933 278493 ...\
305261 374165 374144 407059 279181 ...\
301103 319553 358798 414279 282297 ...\
303032 323821 361486 323163 ...\
349748 374318 392890 293995 ...\
341976 ];

path_ToFile = './data/EMCI_data/fMRI_%d.txt';
path_ToResult = '/home/medialab/Zhewei/MatLabCode/data/EMCI_data/EM_Result%d.txt';


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
