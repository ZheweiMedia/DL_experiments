%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%   Used for VOC2012 images. Change the size to 500*500, then downsampling
%   to 250*250, 125*125, 50*50.
%
%
%
%
%


fileFold = fullfile('~/data/VOCdevkit/VOC2012/SegmentationClass/');
postFix = '*.png';
cd ~/data/VOCdevkit/VOC2012/SegmentationClass/
path = '~/data/VOC_Preprocessed_Data/SegmentationClass/500_500/';
sizeTo = 500;

dirOutput = dir(fullfile(fileFold, postFix));
fileNames = {dirOutput.name};

[m,n] = size(fileNames);
for files = 1:n
    %fileName = strcat(fileNames{1,files},'.jpg');
    [I, map]  = imread(fileNames{1,files});
    I_500 = imresize(I, [sizeTo sizeTo]);
    saveName = strcat(path,fileNames{1,files});
    imwrite(I_500, 'saveName.jpg','jpg');
    
end