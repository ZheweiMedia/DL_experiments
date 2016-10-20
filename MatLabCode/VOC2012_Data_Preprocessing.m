%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%   Used for VOC2012 images. Change the size to 500*500, then downsampling
%   to 250*250, 125*125, 50*50.
%
%
%
%
%

clear all;

fileFold = fullfile('~/data/VOCdevkit/VOC2012/JPEGImages');
postFix = '*.jpg';
cd ~/data/VOCdevkit/VOC2012/JPEGImages/
path = '~/data/VOC_Preprocessed_Data/JPEGImages/50_50/';
sizeTo = 50;

dirInput = dir(fullfile(fileFold, postFix));
fileNames = {dirInput.name};

[m,n] = size(fileNames);
for files = 1:n
    %fileName = strcat(fileNames{1,files},'.jpg');
    I  = imread(fileNames{1,files});
    I_500 = imresize(I, [sizeTo sizeTo]);
    saveName = strcat(path,fileNames{1,files});
    imwrite(I_500, saveName);
    
end