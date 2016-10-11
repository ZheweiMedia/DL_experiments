%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%   Used for VOC2012 images. Change the size to 500*500, then downsampling
%   to 250*250, 125*125, 50*50.
%
%
%
%
%


fileFold = fullfile('~/data/VOCdevkit/VOC2012/SegmentationObject/');
postFix = '*.png';
cd ~/data/VOCdevkit/VOC2012/SegmentationObject/
path = '~/data/VOC_Preprocessed_Data/SegmentationObject/50_50/';
sizeTo = 50;

dirOutput = dir(fullfile(fileFold, postFix));
fileNames = {dirOutput.name};

[m,n] = size(fileNames);
for files = 1:n
    %fileName = strcat(fileNames{1,files},'.jpg');
    [I, map]  = imread(fileNames{1,files});
    [I_500, newmap] = imresize(I, map, [sizeTo sizeTo]);
    saveName = strcat(path,fileNames{1,files});
    imwrite(I_500, newmap,saveName);
    
end