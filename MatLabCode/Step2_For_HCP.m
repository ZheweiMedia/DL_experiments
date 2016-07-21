%%
% 05/27/2016
%
%

% clear all

%%

%%
IID = [ 100307 103515 103818 111312 114924 ...\
117122 118932 119833 120212 125525 128632 130013 ...\
137128 138231 142828 143325 149337 ...\
150423 153429 156637 159239 161731 162329 167743 ...\
182739 191437 192439 192540 194140 197550 ...\
199150 199251 200614 201111 210617 217429 249947 ...\
250427 304020 307127 329440 499566 ...\
530635 559053 585862 638049 665254 672756 ...\
685058 729557 732243 792564 826353 856766 859671 ...\
861456 865363 877168 889579 894673 896778 896879 ...\
901139 917255 937160 ];

class = ['EMOTION'];


path_ToResult = '/home/medialab/Zhewei/MatLabCode/data/LMCI_data/LM_Result%d.txt';


lenthOfFMRI = 176;


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
    Path = strcat('/home/medialab/data/HCP-Q1/tfMRI/',sprintf('%d',fileID),'/',class,'/',strcat(sprintf('%d',fileID),'_',class,'.txt'));
    IIDfilename = Path;
    IID_data = importdata(IIDfilename);
    IID_data = sort(IID_data);
    IID_data = IID_data;

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
    
    fileID = IID(ifile);
    Path = strcat('/home/medialab/data/HCP-Q1/tfMRI/',sprintf('%d',fileID),'/',class,'/',strcat(sprintf('%d',fileID),'_',class,'_','results','.txt'));
    IIDfilename = Path;
    
    fileWrite = fopen(IIDfilename,'w');


    fprintf(fileWrite,'===========%d================\n',IID(ifile));
    display(ifile);

    nii_atlas = load_untouch_nii('/home/medialab/spm12/atlas/AAL2.nii');% atlas
    [x,y,z] = size(nii_atlas.img);

    for ii = 1:lenthOfFMRI
        frame = data{1,ifile}{ii,1};
        % # Should sort at here
        fid = fopen(frame);
        fprintf(fileWrite,'========================%d===============\n',ii);
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
